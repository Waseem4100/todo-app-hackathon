import os
from huggingface_hub import HfApi
import shutil
import tempfile

# Initialize the API
api = HfApi()

# Define the repository ID (your Space) - using the URL you provided
repo_id = "Waseem4100/todoAPI2"  # Based on your space URL: https://waseem4100-todoapi2.hf.space

# Source backend directory
source_dir = r"D:\Coding\hackathons\todo-app\backend"

# Create a temporary directory for the upload
with tempfile.TemporaryDirectory() as temp_dir:
    # Copy backend files to temp directory
    temp_backend_dir = os.path.join(temp_dir, "backend_upload")
    shutil.copytree(source_dir, temp_backend_dir)
    
    # Upload all files from the backend directory to the Space
    for root, dirs, files in os.walk(temp_backend_dir):
        for file in files:
            local_file_path = os.path.join(root, file)
            
            # Calculate the relative path from the backend directory
            relative_file_path = os.path.relpath(local_file_path, temp_backend_dir)
            
            # Skip cache directories and test databases
            if "__pycache__" in local_file_path or ".pytest_cache" in local_file_path or "todo_test.db" in local_file_path:
                continue
            
            # Upload the file to the Space
            print(f"Uploading {relative_file_path}...")
            api.upload_file(
                path_or_fileobj=local_file_path,
                path_in_repo=relative_file_path,
                repo_id=repo_id,
                repo_type="space"
            )

print("All backend files uploaded successfully to https://waseem4100-todoapi2.hf.space!")