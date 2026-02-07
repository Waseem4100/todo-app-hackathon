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

    # Upload the updated app.py file with better error handling
    local_file_path = "D:/Coding/hackathons/todo-app/hf-backend/app.py"
    repo_file_path = "app.py"
    
    print(f"Uploading updated {repo_file_path} with improved error handling...")
    api.upload_file(
        path_or_fileobj=local_file_path,
        path_in_repo=repo_file_path,
        repo_id=repo_id,
        repo_type="space"
    )

    print()
    print("[SUCCESS] Updated app.py uploaded to https://waseem4100-todoapi2.hf.space!")
    print("Added better error handling for database initialization to prevent startup crashes.")
    print("Added logging to help debug any remaining issues.")

except Exception as e:
    print(f"[ERROR] Error during upload: {str(e)}")
    import traceback
    traceback.print_exc()