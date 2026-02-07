import os
from huggingface_hub import login, HfApi
import shutil
import tempfile

# The token you provided
# NOTE: This is a placeholder token - replace with your actual token when running locally
token = "YOUR_HF_TOKEN_HERE"

try:
    # Login using the token
    login(token=token)
    print("[SUCCESS] Authentication successful!")

    # Initialize the API
    api = HfApi()

    # Define the repository ID (your Space)
    repo_id = "Waseem4100/todoAPI2"  # Based on your space URL: https://waseem4100-todoapi2.hf.space

    # Source directory - using the hf-backend which has our fixed files
    source_dir = r"D:\Coding\hackathons\todo-app\hf-backend"

    print(f"Uploading fixed backend files to: {repo_id}")

    # Upload all files from the hf-backend directory to the Space
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            local_file_path = os.path.join(root, file)

            # Calculate the relative path from the hf-backend directory
            relative_file_path = os.path.relpath(local_file_path, source_dir)

            # Skip cache directories and test databases
            if ("__pycache__" in local_file_path or 
                ".pytest_cache" in local_file_path or 
                "todo_test.db" in local_file_path or
                "__pycache__" in relative_file_path):
                continue

            # Upload the file to the Space
            print(f"Uploading {relative_file_path}...")
            api.upload_file(
                path_or_fileobj=local_file_path,
                path_in_repo=relative_file_path,
                repo_id=repo_id,
                repo_type="space"
            )

    print()
    print("[SUCCESS] Fixed backend files uploaded to https://waseem4100-todoapi2.hf.space!")
    print("Uploaded files from hf-backend directory with Python path fixes for Hugging Face Spaces.")
    print("This should resolve the ModuleNotFoundError by properly configuring the Python path.")
    print("The application should now start successfully on Hugging Face Spaces.")

except Exception as e:
    print(f"[ERROR] Error during upload: {str(e)}")
    import traceback
    traceback.print_exc()