import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
    
)


def get_files_info(working_directory,directory="."):

    try :
        
        abslute_path = os.path.abspath(working_directory)

        full_path = os.path.normpath(os.path.join(abslute_path,directory))



        if abslute_path != os.path.commonpath([abslute_path,full_path]):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        elif not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        files = os.listdir(full_path)
        temp_list = []
            
        formatted = []

        for file in files:
            file_path = os.path.join(full_path, file)
            name = file
            size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            formatted.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
        return '\n'.join(formatted)
            
    except Exception as e :
        return f"Error: {e}"
