import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file
from functions.get_files_info import schema_get_files_info, available_functions, get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    funct_dict = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
    }
    function_name = funct_dict.get(function_call_part.name)
    if function_name is None:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)
    args = dict(function_call_part.args)

    if function_call_part.name == "get_files_info" and args.get("directory") == ".":
        args["directory"] = "./calculator"

    args["working_directory"] = "./calculator"  # <--- This stays OUTSIDE the if, always add it!
    function_result = function_name(**args)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": function_result},
        )
    ],
)
    

if len(sys.argv) < 2:
    print("Missing an argument after the name of the file, program is about to close")
    sys.exit(1)
else:
    user_prompt = sys.argv[1]
    is_verbose = "--verbose" in sys.argv
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt))
    if response.function_calls:
        for function in response.function_calls:
            result = call_function(function, is_verbose)
            if (result and
            result.parts and
            len(result.parts) > 0 and
            hasattr(result.parts[0], 'function_response') and
            hasattr(result.parts[0].function_response, 'response')):
             if is_verbose:
                print(f"-> {result.parts[0].function_response.response}")
            else:
                raise Exception("Unexpected function call result structure!")

        if is_verbose:
            print(f"""User prompt: {user_prompt} \nPrompt tokens: {response.usage_metadata.prompt_token_count} \nResponse tokens: {response.usage_metadata.candidates_token_count}""")
    else:
        print(response.text)

