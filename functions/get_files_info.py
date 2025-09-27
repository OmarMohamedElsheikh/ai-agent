import os

def get_files_info(working_dir, directory="."):

    working_dir = os.path.abspath(working_dir)
    full_path = os.path.abspath(os.path.join(working_dir, directory))

    if not full_path.startswith(working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
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
