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
    sketches = list(SKETCH_DIR.glob("*.png"))
    print(f"📋 Found {len(sketches)} images to process.")

    for i, sketch_path in enumerate(sketches):
        name = sketch_path.name.replace(".png", "")
        prompt_path = PROMPT_DIR / f"{name}-prompt.txt"
        output_file = OUTPUT_DIR / f"{name}-output.md"

        if not prompt_path.exists():
            continue

        if output_file.exists():
            # temporary measure for texting
            print(f"{output_file} already exists. Moving to next drawing-prompt pair...")

        max_retries = 5
        retry_delay = 10 # Base wait time in seconds
        
        for attempt in range(max_retries):
            try:
                print(f"🔄 [{i+1}/{len(sketches)}] Processing {name} (Attempt {attempt+1})...")
                
                # Load assets
                prompt_text = prompt_path.read_text(encoding="utf-8")
                image_bytes = sketch_path.read_bytes()

                # Generate
                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=[
                        prompt_text,
                        types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                    ]
                )

                # Save
                output_file.write_text(response.text, encoding="utf-8")
                
                print(f"✅ Success!")
                
                # MANDATORY BREATHING ROOM: 
                # Prevents the 429 'Too Many Requests' seen in your dashboard
                time.sleep(4) 
                break 

            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg or "503" in err_msg:
                    # Exponential backoff: 10s, 20s, 30s... plus a bit of randomness
                    wait = (retry_delay * (attempt + 1)) + random.uniform(1, 5)
                    print(e)
                    print(f"⚠️ Rate limited or Server Busy. Sleeping {wait:.1f}s...")
                    time.sleep(wait)
                else:
                    print(f"❌ Permanent Error for {name}: {e}")
                    break
        else:
            print(f"🚫 Failed {name} after {max_retries} attempts.")

if __name__ == "__main__":
    process_with_respect()