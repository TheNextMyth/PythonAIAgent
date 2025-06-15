import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    file = open(target_file_path, 'w')
    file.write(content)
    return f'Successfully wrote to "{target_file_path}" ({len(content)} characters written)'
