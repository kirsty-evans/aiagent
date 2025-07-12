import os
import subprocess

def run_python_file(working_directory, file_path):

    full_path = os.path.join(working_directory, file_path)
    # print(f"Full path: {full_path}")

    abspath_full_path = os.path.abspath(full_path)
    # print(f"Absolute full path: {abspath_full_path}")

    abspath_working_directory = os.path.abspath(working_directory)
    # print(f"Absolute working directory path: {abspath_working_directory}")

    if abspath_full_path.startswith(abspath_working_directory) == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abspath_full_path):
        return f'Error: File "{file_path}" not found.'
    
    if abspath_full_path.endswith('.py') == False:
        return f'Error: "{file_path}" is not a Python file.'
    
    result = subprocess.run(f"uv run {file_path}", timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=abspath_working_directory)

    # Decode the bytes to strings
    stdout_text = result.stdout.decode() if result.stdout else ""
    stderr_text = result.stderr.decode() if result.stderr else ""

    # Build your output string
    output_parts = []
    output_parts.append(f"STDOUT:\n{stdout_text}")
    output_parts.append(f"STDERR:\n{stderr_text}")

    # Check for non-zero exit code
    if result.returncode != 0:
        output_parts.append(f"Process exited with code {result.returncode}")

    # Join the parts or handle the no-output case
    if stdout_text == "" and stderr_text == "":
        return "No output produced."
    else:
        return "\n".join(output_parts)
    

    

