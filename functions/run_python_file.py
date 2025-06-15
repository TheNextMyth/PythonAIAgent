import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File "{target_file_path}" not found.'
    if target_file_path[-3:] != ".py":
        return f'Error: "{target_file_path}" is not a Python file.'
    timeout_length = 30
    subprocess.run(['chmod', '+x', target_file_path])
    try:
        result = subprocess.run(["python", target_file_path], timeout=timeout_length, check=True, capture_output=True, cwd=target_dir)
    except subprocess.CalledProcessError:
        return f'Process exited with code {returncode}'
    except subprocess.TimeoutExpired:
        return f'Process timed out after {timeout_length} seconds'
    except Exception as e:
        return f'Error: executing Python file: {e}'
    else:
        return f'STDOUT: {result.stdout}, STDERR: {result.stderr}'
