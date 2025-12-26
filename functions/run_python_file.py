import os
import subprocess
from google.genai import types
def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_dir = os.path.normpath(
            os.path.join(working_dir_abs,file_path)
        )

        valid_path = (os.path.commonpath([working_dir_abs,target_dir]) == working_dir_abs)

        if not valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Disallow non-Python files
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # ---- Subprocess ----
        command = ["python", target_dir]

        if args is not None:
            command.extend(args)

        def build_output(result):
            parts = []

            if result.returncode != 0:
                parts.append(f"Process exited with code {result.returncode}")

            if not result.stdout and not result.stderr:
                parts.append("No output produced")
            else:
                if result.stdout:
                    parts.append(f"STDOUT:\n{result.stdout}")
                if result.stderr:
                    parts.append(f"STDERR:\n{result.stderr}")

            return "\n".join(parts)
        
        result = subprocess.run(
        command,
        cwd=working_directory,
        capture_output=True,
        text=True,
        timeout=30
        )

        return build_output(result)



    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file relative to the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)
