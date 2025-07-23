import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = ""
    if directory:
        target_dir = os.path.abspath(
            os.path.join(
                abs_working_directory, directory
                ))
    if target_dir and not target_dir.startswith(abs_working_directory):
        return f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{target_dir}" is not a directory'
    
    try:
        dir_content = os.listdir(target_dir)
        result = []
        for item in dir_content:
            item_size = os.path.getsize(os.path.join(target_dir, item))
            is_item_dir = os.path.isdir(os.path.join(target_dir, item))
            result.append(f"- {item}: file_size={item_size} bytes, is_dir={is_item_dir}")

        return "\n".join(result)
    except Exception as e:
        return f"Error: {e}"
    
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


def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(
        os.path.join(
            abs_working_directory, file_path
            ))

    if target_file_path and not target_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{target_file_path}"'
    
    try:
        MAX_CHARS = 10000
        result = []
        with open(target_file_path, "r") as f:
            file_content_str = f.read(MAX_CHARS)
            result.append(file_content_str)

            if f.read() != "":
                result.append(f'[...File "{target_file_path}" truncated at 10000 characters]')

        return "\n".join(result)

    except Exception as e:
        return f"Error: {e}"
    
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="List the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to list the content from, relative to the working directory",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(
        os.path.join(
            abs_working_directory, file_path
            ))

    if target_file_path and not target_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    try:
        if not os.path.exists(target_file_path):
            file_directory = os.path.dirname(target_file_path)

            if not os.path.isdir(file_directory):
                os.makedirs(file_directory)

            with open(target_file_path, "w") as f:
                f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the content to a file - which gets created if it doesn't exist already - constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write the content, created if it doesn't exist, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content which that needs to be written to the file",
            ),
        },
    ),
)