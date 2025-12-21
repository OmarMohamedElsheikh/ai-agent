import os

def write_file(working_directory , file_path , content):
    abslute_path = os.path.abspath(working_directory)
    
    full_path = os.path.normpath(os.path.join(abslute_path,file_path))



    if abslute_path != os.path.commonpath([abslute_path,full_path]):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    elif os.path.isdir(full_path):
        return f'Error: "{file_path}" is a directory'


    os.makedirs(os.path.dirname(full_path),exist_ok=True)

    try :
        with open(full_path,"w") as f :
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e :
        return f"Error: {e}"
