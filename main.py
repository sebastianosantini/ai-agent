import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

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


    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    args = sys.argv[1:]
    if not args:
        print("no args provided...")
        sys.exit(1)
    
    user_prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
    
    if response.function_calls:
        function_called_name = response.function_calls[0].name
        function_called_args = response.function_calls[0].args 

    if response.function_calls:
        print(f"User prompt: {user_prompt}")
        print(f"Calling function: {function_called_name}({function_called_args})")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()