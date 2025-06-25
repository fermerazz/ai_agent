import os

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)    
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
        return f'Error: Cannot read "{target_file}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{target_file}"'
    try:
        MAX_CHARS = 10000
        with open(target_file, "r") as f:
            file_content_str = f.read(MAX_CHARS + 1)
            if len(file_content_str) > MAX_CHARS:
                truncated_content = file_content_str[:MAX_CHARS] + f'[...File "{target_file}" truncated at 10000 characters]'
                return truncated_content
            else:
                return file_content_str
    except Exception as e:
        return f"Error: {str(e)}"