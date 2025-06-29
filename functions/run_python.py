import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)    
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(target_file):
            return f'Error: File "{file_path}" not found.'

        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        result = subprocess.run(["python3", target_file], timeout=30, capture_output=True, text=True, cwd=abs_working_dir)
        if not result.stderr and not result.stdout:
            return f'No output produced.'
        
        output = f"STDOUT: {result.stdout}, STDERR: {result.stderr}"
        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"
        return output
    except Exception as e:
        return f'Error: executing Python file: {e}'