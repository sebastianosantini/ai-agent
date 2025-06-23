import os, shlex, subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = ""
    if file_path:
        target_file_path = os.path.abspath(
            os.path.join(
                abs_working_directory, file_path
                ))
    if target_file_path and not target_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File "{file_path}" not found.'
    if not target_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    result = []
    TIMEOUT = 30
    exe_command = f"python3 {file_path}"
    args = shlex.split(exe_command)
    try:
        return_values = subprocess.run(args, cwd=working_directory, timeout=TIMEOUT)

        stdout = f"STDOUT: {return_values.stdout}" if return_values.stdout else "No output produced."
        result.append(stdout)
        stderr = f"STDERR: {return_values.stderr}"
        result.append(stderr)
        return_code = return_values.returncode if return_values.returncode != 0 else f"Process exited with code {return_values.returncode}"
        result.append(return_code)

        return "\n".join(result)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the program to run, relative to the working directory",
            ),
        },
    ),
)


