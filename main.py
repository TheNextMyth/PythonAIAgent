import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
verbose = False
n = len(sys.argv)

if n > 1:
    user_prompt = sys.argv[1]
else:
    print("No prompt was entered.")
    sys.exit(1)

for i in range(1, n):
    if sys.argv[i] == "--verbose":
        verbose = True

client = genai.Client(api_key=api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages,
)
print(response.text)

if verbose:
    print("Prompt:", user_prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
