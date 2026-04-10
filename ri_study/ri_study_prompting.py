import os
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Configuration
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Directory Setup
SKETCH_DIR = Path("drawings")
PROMPT_DIR = Path("custom-images")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def run_batch_processing():
    # Find all sketches
    sketches = list(SKETCH_DIR.glob("*.png"))
    
    if not sketches:
        print("No sketches found in the /sketches folder.")
        return

    for sketch_path in sketches:
        # Determine the base name
        name = sketch_path.name.replace("-sketch.png", "")
        prompt_path = PROMPT_DIR / f"{name}-prompt.txt"

        if not prompt_path.exists():
            print(f"⚠️  Missing prompt for: {name}. Skipping...")
            continue

        print(f"🚀 Processing: {name}")

        try:
            # Read files
            prompt_text = prompt_path.read_text(encoding="utf-8")
            image_parts = [
                {
                    "mime_type": "image/png",
                    "data": sketch_path.read_bytes()
                }
            ]

            # Generate and save
            response = model.generate_content([prompt_text, image_parts[0]])
            
            output_file = OUTPUT_DIR / f"{name}-output.md"
            output_file.write_text(response.text, encoding="utf-8")
            
            print(f"✅ Success: {output_file}")

        except Exception as e:
            print(f"❌ Error with {name}: {e}")

if __name__ == "__main__":
    run_batch_processing()