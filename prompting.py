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
PROMPT_PATH = Path("prompts/site_parsing.md")
SKETCH_PATH = Path("samples/sample_bronx_drawing.png")
OUTPUT_PATH = Path("sample_output.md")

# Client Setup
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MAX_RETRIES = 3

def process_sketch():

    if not SKETCH_PATH.exists():
        print(f"{SKETCH_PATH} does not exist")
        return
    
    if not PROMPT_PATH.exists():
        print(f"{PROMPT_PATH} does not exist")
        return

    for attempt in range(MAX_RETRIES):
        try:
            print(f"🔄 [Processing {SKETCH_PATH} (Attempt {attempt+1})...")
            
            prompt_text = PROMPT_PATH.read_text(encoding="utf-8")
            image_bytes = SKETCH_PATH.read_bytes()

            response = client.models.generate_content(
                model=MODEL_ID,
                contents=[
                    prompt_text,
                    types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                ]
            )

            OUTPUT_PATH.write_text(response.text, encoding="utf-8")
            print(f"Success: {OUTPUT_PATH.name}")

        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "503" in err_msg:
                # If we hit a wall, wait a full minute + jitter
                wait = 60 + random.uniform(5, 15)
                print(f"🚨 API Overloaded. Sleeping {wait:.1f}s before retry...")
                time.sleep(wait)
            else:
                print(f"❌ Permanent Error: {e}")
                break

if __name__ == "__main__":
    process_sketch()