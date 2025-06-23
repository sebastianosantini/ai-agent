from function.get_files_info import schema_get_files_info, schema_get_file_content, schema_write_file
from function.run_python_file import schema_run_python_file
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)