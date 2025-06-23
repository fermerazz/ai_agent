import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)



if len(sys.argv) < 2:
    print("Missing an argument after the name of the file, program is about to close")
    sys.exit(1)
else:
    user_prompt = sys.argv[1]
    is_verbose = "--verbose" in sys.argv
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(model='gemini-2.0-flash-001',
                                           contents=messages)
    if is_verbose == True:
        print(response.text)
        print(f"""User prompt: {user_prompt} \nPrompt tokens: {response.usage_metadata.prompt_token_count} \nResponse tokens: {response.usage_metadata.candidates_token_count}""")
    else:
        print(response.text)
