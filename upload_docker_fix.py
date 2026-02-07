import os
from huggingface_hub import login, HfApi

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
    
    # Upload the fixed files
    files_to_upload = [
        ("D:/Coding/hackathons/todo-app/backend/Dockerfile", "Dockerfile"),
        ("D:/Coding/hackathons/todo-app/backend/Procfile", "Procfile")
    ]
    
    print(f"Uploading fixed files to: {repo_id}")
    
    for local_path, repo_path in files_to_upload:
        print(f"Uploading {repo_path}...")
        api.upload_file(
            path_or_fileobj=local_path,
            path_in_repo=repo_path,
            repo_id=repo_id,
            repo_type="space"
        )
    
    print()
    print("[SUCCESS] Fixed files uploaded to https://waseem4100-todoapi2.hf.space!")
    print("Changed the CMD to use 'python -m uvicorn' to ensure proper module resolution.")
    print("The application should now start successfully.")

except Exception as e:
    print(f"[ERROR] Error during upload: {str(e)}")
    import traceback
    traceback.print_exc()