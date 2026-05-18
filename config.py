import os
import sys
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Security Gatekeeper: Stop execution immediately if the API key is missing
if not GEMINI_API_KEY:
    print("❌ Security Error: GEMINI_API_KEY is missing from your .env file!")
    print("Please generate a key at https://aistudio.google.com/ and add it to .env")
    sys.exit(1)