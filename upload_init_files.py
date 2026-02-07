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
    
    # Upload the __init__.py files to make directories proper Python packages
    files_to_upload = [
        ("D:/Coding/hackathons/todo-app/backend/src/__init__.py", "src/__init__.py"),
        ("D:/Coding/hackathons/todo-app/backend/src/api/__init__.py", "src/api/__init__.py"),
        ("D:/Coding/hackathons/todo-app/backend/src/api/routes/__init__.py", "src/api/routes/__init__.py"),
        ("D:/Coding/hackathons/todo-app/backend/src/database/__init__.py", "src/database/__init__.py"),
        ("D:/Coding/hackathons/todo-app/backend/src/models/__init__.py", "src/models/__init__.py"),
        ("D:/Coding/hackathons/todo-app/backend/src/services/__init__.py", "src/services/__init__.py")
    ]
    
    print(f"Uploading __init__.py files to: {repo_id}")
    
    for local_path, repo_path in files_to_upload:
        print(f"Uploading {repo_path}...")
        api.upload_file(
            path_or_fileobj=local_path,
            path_in_repo=repo_path,
            repo_id=repo_id,
            repo_type="space"
        )
    
    print()
    print("[SUCCESS] All __init__.py files uploaded to https://waseem4100-todoapi2.hf.space!")
    print("Added missing __init__.py files to make directories proper Python packages.")
    print("This should resolve the 'No module named src.api' error.")
    print("The application should now start successfully.")

except Exception as e:
    print(f"[ERROR] Error during upload: {str(e)}")
    import traceback
    traceback.print_exc()