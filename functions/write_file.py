import os 

def write_file(working_directory, file_path, content):
    abs_path = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([abs_path, target_file]) != abs_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        if not os.path.exists(file_path):
            dir = os.dirname(target_file)


    except Exception as e:
        return f"Error: {str(e)}"