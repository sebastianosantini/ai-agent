import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from function.get_files_info import get_files_info, get_file_content, write_file
from function.run_python_file import run_python_file
from prompts import system_prompt
from functions import available_functions


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)
    
    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_code(client, messages, verbose)

def generate_code(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        
        if not function_call_result.parts[0].function_response.response:
            raise Exception("no response found.")
        
        if function_call_result.parts[0].function_response.response and verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")



def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    fucntion_args = function_call_part.args
    fucntion_args["working_directory"] = "./calculator"

    match function_call_part.name:
        case "get_files_info":
            function_result = get_files_info(**fucntion_args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result}
                    )
                ],
            )
        case "get_file_content":
            function_result = get_file_content(**fucntion_args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result}
                    )
                ],
            )
        case "run_python_file":
            function_result = run_python_file(**fucntion_args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result}
                    )
                ],
            )
        case "write_file":
            function_result = write_file(**fucntion_args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": function_result}
                    )
                ],
            )
        
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )
        


if __name__ == "__main__":
    main()