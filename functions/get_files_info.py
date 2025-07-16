import os

def get_files_info(working_directory, directory=None):

    # print(f"Working directory: {working_directory}")
    # print(f"Directory to list: {directory}")

    full_path = os.path.join(working_directory, directory)
    # print(f"Full path: {full_path}")

    abspath_full_path = os.path.abspath(full_path)
    # print(f"Absolute full path: {abspath_full_path}")

    abspath_working_directory = os.path.abspath(working_directory)
    # print(f"Absolute working directory path: {abspath_working_directory}")

    if abspath_full_path.startswith(abspath_working_directory) == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    

    elif not os.path.isdir(abspath_full_path):
        return f'Error: "{directory}" is not a directory'
    
    else:
        contents_string = ""
        # print(f"the list is {os.listdir(abspath_full_path)}")
        try:
            for item in os.listdir(abspath_full_path):
                # print(f"checking item: {item}")
                item_path = os.path.join(abspath_full_path, item)
                contents_string += (f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}\n")
                # print(f"The string returned so far is {contents_string}")
            return contents_string
        except:
            return f'Error: Cannot get directory contents for {abspath_full_path}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

