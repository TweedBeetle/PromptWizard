import os
import tempfile
import subprocess


# Python REPL to execute code. taken from NuminaMath Solution
class PythonREPL:
    def __init__(self, timeout=8):
        self.timeout = timeout

    def __call__(self, query):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "tmp.py")
            with open(temp_file_path, "w", encoding="utf-8") as f:
                f.write(query)

            try:
                result = subprocess.run(
                    ["python3", temp_file_path],
                    capture_output=True,
                    check=False,
                    text=True,
                    timeout=self.timeout,
                )
            except subprocess.TimeoutExpired:
                return False, f"Execution timed out after {self.timeout} seconds."

            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            if result.returncode == 0:
                return True, stdout
            else:
                # Process the error message to remove the temporary file path
                # This makes the error message cleaner and more user-friendly
                error_lines = stderr.split("\n")
                cleaned_errors = []
                for line in error_lines:
                    if temp_file_path in line:
                        # Remove the path from the error line
                        line = line.replace(temp_file_path, "<temporary_file>")
                    cleaned_errors.append(line)
                cleaned_error_msg = "\n".join(cleaned_errors)
                # Include stdout in the error case
                combined_output = f"{stdout}\n{cleaned_error_msg}" if stdout else cleaned_error_msg
                return False, combined_output
