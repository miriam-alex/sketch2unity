import os
from dotenv import load_dotenv
from google import genai

# 1. Setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def test_model_traffic():
    print("🔍 Fetching available models...")
    
    # Get all models that support content generation
    available_models = []
    for m in client.models.list():
        # Only test models that actually support text generation
        if "generateContent" in m.supported_actions:
            available_models.append(m.name)

    print(f"Found {len(available_models)} candidate models.\n")

    for model_id in available_models:
        print(f"--- Testing: {model_id} ---")
        
        try:
            # Simple health check prompt
            response = client.models.generate_content(
                model=model_id,
                contents="ping"
            )
            
            # Print a snippet of the response to verify it's 'thinking'
            print(f"✅ STATUS: ONLINE")
            print(f"💬 Response: {response.text[:50]}...")

        except Exception as e:
            # This captures 429 (Rate Limit/Traffic), 503 (Overloaded), and 404
            print(f"❌ STATUS: FAILED/HIGH TRAFFIC")
            print(f"⚠️  Error: {e}")

        # Manual control to continue or stop
        user_input = input("\nHit [Enter] to test next model, or type 'q' to quit: ").lower()
        if user_input == 'q':
            print("Exiting tester.")
            break
        print("\n" + "="*30 + "\n")

if __name__ == "__main__":
    test_model_traffic()