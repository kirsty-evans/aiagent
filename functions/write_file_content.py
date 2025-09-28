import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    # print(f"Full path: {full_path}")

    abspath_full_path = os.path.abspath(full_path)
    # print(f"Absolute full path: {abspath_full_path}")

    abspath_working_directory = os.path.abspath(working_directory)
    # print(f"Absolute working directory path: {abspath_working_directory}")

    if abspath_full_path.startswith(abspath_working_directory) == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    

    if not os.path.exists(os.path.dirname(abspath_full_path)):
        try:
            os.makedirs(os.path.dirname(abspath_full_path))
        except Exception as e:
            return f'Error creating directory for file "{file_path}": {e}'
        
    with open(abspath_full_path, "w") as f:
        try:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f'Error writing to file "{file_path}": {e}'
        
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the specified working directory, creating directories as needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that will be written to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)
