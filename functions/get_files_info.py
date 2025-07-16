import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory
        
    if not os.path.abspath(directory).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    try:
        files = os.listdir(directory)
        all_files = []
        for file in files:
            full_path = os.path.join(directory, file)
            size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            all_files.append(f"- {file}: file_size={size}, is_dir={is_dir}")
        return "\n".join(all_files) 
    except Exception as e:
        return f"Error: {str(e)}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of the file at the specified path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties= {
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose contents will be returned, relative to the working directory.",
            )
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the file at the specified path with the provided content",
    parameters= types.Schema(
        type=types.Type.OBJECT,
        properties= {
            "file_path": types.Schema(
                type=types.Type.STRING,
                description= "The path to the file we wan to write in"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description= "The content we aim to write into the file"
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Attemps to run the python file with the provided file path and optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the script."
            ),
        }
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)