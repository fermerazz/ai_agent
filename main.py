import os, sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


if len(sys.argv) < 2:
    print("Missing an argument after the name of the file, program is about to close")
    sys.exit(1)
else:
    response = client.models._generate_content(model='gemini-2.0-flash-001',
                                           contents=sys.argv[1])
    print(response.text)
    print(f"""Prompt tokens: {response.usage_metadata.prompt_token_count}
    Response tokens: {response.usage_metadata.candidates_token_count} """)