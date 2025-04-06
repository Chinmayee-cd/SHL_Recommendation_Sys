import os
import sys
import subprocess
import webbrowser
from pathlib import Path
import google.generativeai as genai  # type: ignore
from dotenv import load_dotenv  # type: ignore

def check_python_version():
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)
    print("✅ Python version check passed.")

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies.")
        sys.exit(1)

def check_env_file():
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found. Creating one...")
        with open(env_path, "w") as f:
            f.write("# Google Gemini API Key\n")
            f.write("# Replace with your actual API key from https://ai.google.dev/\n")
            f.write("GEMINI_API_KEY=your_api_key_here\n")
        print("✅ Created .env file. Please edit it to add your Gemini API key.")
    else:
        with open(env_path, "r") as f:
            content = f.read()
            if "your_api_key_here" in content:
                print("⚠️ Gemini API key not set in .env file.")
                print("Please edit the .env file to add your API key.")
            else:
                print("✅ .env file found with API key.")

def open_gemini_api_page():
    print("Opening Gemini API page in your browser...")
    webbrowser.open("https://ai.google.dev/")

def main():
    print("=" * 50)
    print("SHL Assessment Recommender - Setup")
    print("=" * 50)
    
    check_python_version()
    install_dependencies()
    check_env_file()
    open_gemini_api_page()
    
    # Load environment variables
    load_dotenv()

    # Configure Gemini API
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    # List available models
    try:
        for m in genai.list_models():
            print(f"Model: {m.name}")
        print("\nAPI connection successful!")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print("\nSetup completed!")
    print("\nTo run the application:")
    print("1. Edit the .env file to add your Gemini API key")
    print("2. Start the API server: uvicorn api.main:app --reload")
    print("3. In a separate terminal, start the Streamlit app: streamlit run app/main.py")
    print("\nEnjoy using the SHL Assessment Recommender!")

if __name__ == "__main__":
    main() 