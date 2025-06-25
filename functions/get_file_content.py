import os

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)    
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'