import os
from google.genai import types


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    max_file_length = 10000
    file = open(target_file_path, "r")
    file_contents = file.read()
    if len(file_contents) > max_file_length:
        return file_contents[:max_file_length], f'File "{file_path}" truncated at {max_file_length} characters'
    else:
        return file_contents

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of a file and return its contents as a string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose contents we want to read.",
            ),
        },
    ),
)         
