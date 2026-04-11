import os
import time
import random
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Configuration
MODEL_ID = "gemini-2.5-flash"
SKETCH_DIR = Path("drawings")
PROMPT_DIR = Path("prompts")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Client Setup
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def process_with_respect():
    # Only grab images that don't have a markdown output yet
    sketches = [s for s in SKETCH_DIR.glob("*.png") 
                if not (OUTPUT_DIR / f"{s.stem}-output.md").exists()]
    
    print(f"📋 Found {len(sketches)} new images to process.")

    for i, sketch_path in enumerate(sketches):
        name = sketch_path.stem  # Get filename without extension
        prompt_path = PROMPT_DIR / f"{name}-prompt.txt"
        output_file = OUTPUT_DIR / f"{name}-output.md"

        if not prompt_path.exists():
            print(f"⚠️ Prompt missing for {name}, skipping...")
            continue

        max_retries = 3
        # In 2026, 30s is the 'Safe Zone' for free tier multimodal requests
        base_cooldown = 30 
        
        for attempt in range(max_retries):
            try:
                print(f"🔄 [{i+1}/{len(sketches)}] Processing {name} (Attempt {attempt+1})...")
                
                prompt_text = prompt_path.read_text(encoding="utf-8")
                image_bytes = sketch_path.read_bytes()

                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=[
                        prompt_text,
                        types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                    ]
                )

                output_file.write_text(response.text, encoding="utf-8")
                print(f"✅ Success: {output_file.name}")
                
                # CRITICAL: Wait 30s to allow the "Tokens Per Minute" bucket to refill.
                # Image processing is token-heavy!
                if i < len(sketches) - 1:
                    print(f"⏳ Cooling down for {base_cooldown}s...")
                    time.sleep(base_cooldown)
                break 

            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg or "503" in err_msg:
                    # If we hit a wall, wait a full minute + jitter
                    wait = 60 + random.uniform(5, 15)
                    print(f"🚨 API Overloaded. Sleeping {wait:.1f}s before retry...")
                    time.sleep(wait)
                else:
                    print(f"❌ Permanent Error for {name}: {e}")
                    break
        else:
            print(f"🚫 Giving up on {name} after {max_retries} attempts.")

if __name__ == "__main__":
    process_with_respect()