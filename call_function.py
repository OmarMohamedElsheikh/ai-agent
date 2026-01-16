from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file 
from functions.get_file_content import schema_get_file_content


from google.genai import types


available_functions = types.Tool(
    function_declarations=[schema_get_files_info,schema_get_file_content,schema_write_file,schema_run_python_file],

)


def call_function(function_call , verbose=False):

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else :
        print(f" - Calling function: {function_call.name}")

    functions = {
        "write_file": write_file
        ,"get_file_content": get_file_content
        ,"run_python_file": run_python_file
        ,"get_files_info": get_files_info
    }

    function_name = function_call.name 

    if function_name not in functions :
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    function_args = dict(function_call.args)
    working_directory = "./calculator"
    function_args["working_directory"] = working_directory

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
