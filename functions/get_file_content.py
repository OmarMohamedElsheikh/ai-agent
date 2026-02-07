import os 
from google.genai import types
from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="return the content of a spacific file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get content, relative to the working directory.",
            )
        }
    )
)

def get_file_content(working_directory, file_path):

    try :
        
        abslute_path = os.path.abspath(working_directory)

        full_path = os.path.normpath(os.path.join(abslute_path,file_path))
        if abslute_path != os.path.commonpath([abslute_path,full_path]):
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(full_path):
            return f'Error: "{file_path}" is not a regular file'

        with open(full_path,"r") as f:
            content = f.read(MAX_CHARS)
            if os.path.getsize(full_path) > MAX_CHARS:
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return content
    except Exception as e : 
        return f"Error: {e}"
