import os
from huggingface_hub import HfApi

# Initialize the API
api = HfApi()

# Define the repository ID (your Space)
repo_id = "Waseem4100/todoAPI2"

# Local directory containing the files to upload
local_dir = r"D:\Coding\hackathons\todo-app\hf-backend"

# Upload all files from the local directory to the Space
for root, dirs, files in os.walk(local_dir):
    for file in files:
        local_file_path = os.path.join(root, file)
        
        # Calculate the relative path from the local directory
        relative_file_path = os.path.relpath(local_file_path, local_dir)
        
        # Upload the file to the Space
        print(f"Uploading {relative_file_path}...")
        api.upload_file(
            path_or_fileobj=local_file_path,
            path_in_repo=relative_file_path,
            repo_id=repo_id,
            repo_type="space"
        )

print("All files uploaded successfully!")