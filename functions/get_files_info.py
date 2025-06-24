import os

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