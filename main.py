import os
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    print("no content provided...")
    exit(1)

if "main.py" in sys.argv:
    sys.argv.remove("main.py")

content = " ".join(sys.argv)

response = client.models.generate_content(model="gemini-2.0-flash-001", contents=content)

print(response.text)
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}\n")