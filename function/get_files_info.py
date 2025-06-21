import os

def get_files_info(working_directory, directory=None):
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = ""
    if directory:
        target_dir = os.path.abspath(os.path.join(abs_working_directory, directory))
    if target_dir and not target_dir.startswith(abs_working_directory):
        return f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{target_dir}" is not a directory'
    
    try:
        dir_content = os.listdir(target_dir)
        result = []
        for items in dir_content:
            result.append(f"- {items}: file_size={os.path.getsize(os.path.join(target_dir, items))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, items))}")

        return "\n".join(result)
    except Exception as e:
        return f"Error: {e}"

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

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

            if f.read() is not None:
                result.append(f'[...File "{target_file_path}" truncated at 10000 characters]')

        return "\n".join(result)

    except Exception as e:
        return f"Error: {e}"

        