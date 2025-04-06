import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY", "").strip()

print("\n=== Key Verification ===")
print(f"Key exists: {bool(api_key)}")
print(f"Key length: {len(api_key)} chars")
print(f"First 5 chars: {api_key[:5]}")  # Should be "AIzaS"
print(f"Last 5 chars: {api_key[-5:]}")  # Should be "bgUM"

try:
    # 2. Simple configuration (no timeout needed)
    genai.configure(api_key=api_key)
    
    # 3. Test with simple generation
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Reply with just the word 'SUCCESS'")
    
    print(f"\n✅ Response: {response.text}")
    
except Exception as e:
    print(f"\n❌ Failed: {type(e).__name__}: {str(e)}")
    
    # Specific error guidance
    if "API_KEY_INVALID" in str(e):
        print("Fix: Regenerate at https://aistudio.google.com/app/apikey")
    elif "quota" in str(e).lower():
        print("Fix: Check quota at Google Cloud Console")
    elif "503" in str(e):
        print("Fix: Try with VPN (possible regional restriction)")