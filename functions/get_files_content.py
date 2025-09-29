import os
from google.genai import types
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="return the content in spacific file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get content, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_dir, file_path))

        
        if not full_path.startswith(working_dir):
            return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(full_path) or not os.path.exists(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        if len(content) > 10000:
            return content[:10000] + f'\n[...File "{file_path}" truncated at 10000 characters]'
        
        return content
    except Exception as e:
        return f"Error: {e}"
