"""
Project packager: Creates a clean zip archive of the project.
"""

import os
import zipfile

def create_project_zip(output_zip_path: str = "counterfactual_cyber_deception_project.zip"):
    project_root = os.path.dirname(os.path.abspath(__file__))
    exclude_dirs = {".git", "__pycache__", "venv", ".pytest_cache", ".idea", ".vscode"}
    exclude_files = {output_zip_path, "package_project.py"}

    print(f"Creating zip archive at {output_zip_path}...")
    with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_root):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file in exclude_files or file.endswith(".pyc") or file.endswith(".pyo"):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, project_root)
                zipf.write(full_path, rel_path)
                print(f"  Added: {rel_path}")

    print(f"\nSuccessfully generated zip file: {output_zip_path}")
    print(f"File size: {os.path.getsize(output_zip_path) / 1024:.2f} KB")

if __name__ == "__main__":
    create_project_zip()
