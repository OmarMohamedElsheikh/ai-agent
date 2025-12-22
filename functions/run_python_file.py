import os
import subprocess


def run_python_file(working_directory , file_path , args=None):

    try:
        abslute_path = os.path.abspath(working_directory)
          
        full_path = os.path.normpath(os.path.join(abslute_path,file_path))


        if abslute_path != os.path.commonpath([abslute_path,full_path]):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_path):
            return f'Error: "{file_path}" does not exist'

        elif not os.path.isfile(full_path):
            return f'Error: "{file_path}" is not a regular file.'

        elif not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'


        os.makedirs(os.path.dirname(full_path),exist_ok=True)

        command = ['python',full_path]

        if args :
            command.extend(args)

        completedprocess = subprocess.run(command,capture_output=True,timeout=30,text=True)

        fr = []

        if completedprocess.returncode != 0:
            fr.append(f'Process exited with code {completedprocess.returncode}')

        if completedprocess.stdout:
            fr.append(f'STDOUT: {completedprocess.stdout}')

        if completedprocess.stderr:
            fr.append(f'STDERR: {completedprocess.stderr}')

        if not completedprocess.stdout and not completedprocess.stderr:
            fr.append('No output produced')

        return ' '.join(fr)
        
    except Exception as e :
        return f"Error: executing Python file: {e}"

