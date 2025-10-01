import os 
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_files_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part,verbose=False):
    working_dir = "calculator"


    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    else:
        print(f" - Calling function: {function_call_part.name}")
    
    functions = {
        "write_file": write_file
        ,"get_file_content": get_file_content
        ,"run_python_file": run_python_file
        ,"get_files_info": get_files_info
    }


    function_name = function_call_part.name
    function_args = dict(function_call_part.args)
    function_args["working_directory"] = working_dir
    
    
    if function_call_part.name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )


    function_result = functions[function_name](**function_args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
