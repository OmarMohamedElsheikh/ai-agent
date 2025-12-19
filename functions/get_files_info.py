import os

def get_files_info(working_directory,directory="."):


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
        
