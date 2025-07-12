import os

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