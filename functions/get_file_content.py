import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):

    full_path = os.path.join(working_directory, file_path)
    # print(f"Full path: {full_path}")

    abspath_full_path = os.path.abspath(full_path)
    # print(f"Absolute full path: {abspath_full_path}")

    abspath_working_directory = os.path.abspath(working_directory)
    # print(f"Absolute working directory path: {abspath_working_directory}")

    if abspath_full_path.startswith(abspath_working_directory) == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    

    if not os.path.isfile(abspath_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abspath_full_path, "r") as f:
            
            file_content_string = f.read(config.MAX_CHARS)
            if f.read(1) != '':
                return file_content_string + f'[...File "{file_path}" truncated at 10000 characters]'
            else:
                return file_content_string
            
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'