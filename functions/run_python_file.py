import subprocess
import os
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run a given python scrpit.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="argments to pass to the given python script."
                ,items=types.Schema(type=types.Type.STRING)
            )
            ,"file_path": types.Schema(
                type=types.Type.STRING,
                description="The python script file, relative to the working directory.",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    working_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_dir, file_path))

    if not full_path.startswith(working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", full_path] + args,
            cwd=working_dir,
            capture_output=True,
            text=True,          # auto-decodes stdout/stderr
            timeout=30
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        output_parts = []
        if stdout:
            output_parts.append(f"STDOUT: {stdout}")
        if stderr:
            output_parts.append(f"STDERR: {stderr}")
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
