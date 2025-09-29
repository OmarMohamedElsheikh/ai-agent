import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write content in spacific given file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content to write in the file."
            )
            ,"file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write content to it, relative to the working directory.",
            ),
        },
    ),
)


def write_file(working_directory , file_path , content):

    try:
        working_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_dir, file_path))

#        if not os.path.exists(full_path):
#            with open(full_path, "w") as file:
#                pass

        
        if not full_path.startswith(working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(full_path) :
            return f'Error: File is not a regular file: "{file_path}"'

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path,"w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'



    except Exception as e:
        return f"Error: {e}"
