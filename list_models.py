import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    print("❌ API_KEY not found in environment variables.")
    # Try to load from .env file directly if os.getenv failed due to context
    print("Checking .env file content directly...")
    try:
        with open(".env", "r") as f:
            content = f.read()
            if "API_KEY" in content:
                print("Found API_KEY in .env file (raw text check).")
                for line in content.splitlines():
                    if line.startswith("API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        break
    except Exception as e:
        print(f"Error reading .env: {e}")

if not api_key:
    print("CRITICAL: Cannot list models without API Key.")
else:
    print(f"Using API Key: {api_key[:5]}...{api_key[-4:]}")
    genai.configure(api_key=api_key)
    print("Listing available models:")
    try:
        found_any = False
        for m in genai.list_models():
            print(f"- {m.name} (Methods: {m.supported_generation_methods})")
            found_any = True
        if not found_any:
            print("No models found. Check API key permissions.")
    except Exception as e:
        print(f"Error listing models: {e}")
