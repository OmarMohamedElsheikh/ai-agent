from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types




def main():
    if len(sys.argv) < 2 :
        print("usage: python3 main.py [prompet]")
        exit(1)
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    user_prompet = " ".join(sys.argv[1:])
    system_prompt = """
    You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files    
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    Messages = [
        types.Content(role="user",parts=[types.Part(text=user_prompet)])
    ]
    load_dotenv()
    api_key= os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
            
        ]
    )
    def req(client,messages,verbose):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt,tools=[available_functions]),
            
)
    
#        nonlocal vrep
        if verbose:
        
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
            print(f"User prompt: {user_prompet}\n")
        print(response.text) 
        if hasattr(response,"function_calls") and response.function_calls:
            for fc in response.function_calls:
                print(f"Calling function: {fc.name}({fc.args})")    
    req(client,Messages,verbose)
if __name__ == "__main__":
    main()
