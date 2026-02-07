import os
from huggingface_hub import login
import getpass

print("Hugging Face Space Uploader for Todo Backend")
print("="*50)
print("This script will upload your backend files to: https://waseem4100-todoapi2.hf.space")
print()

# Ask for token securely
print("Please enter your Hugging Face token.")
print("You can get one from: https://huggingface.co/settings/tokens")
token = getpass.getpass("Token: ")

if not token.strip():
    print("No token entered. Exiting.")
    exit(1)

try:
    # Login using the token
    login(token=token)
    print("✓ Authentication successful!")
    
    # Now proceed with the upload
    from huggingface_hub import HfApi
    import shutil
    import tempfile
    
    # Initialize the API
    api = HfApi()
    
    # Define the repository ID (your Space)
    repo_id = "Waseem4100/todoAPI2"  # Based on your space URL
    
    # Source backend directory
    source_dir = r"D:\Coding\hackathons\todo-app\backend"
    
    print(f"Preparing to upload backend files from: {source_dir}")
    print(f"Target repository: {repo_id}")
    print()
    
    # Create a temporary directory for the upload
    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy backend files to temp directory
        temp_backend_dir = os.path.join(temp_dir, "backend_upload")
        shutil.copytree(source_dir, temp_backend_dir)
        
        # Count total files to upload
        total_files = sum([len(files) for _, _, files in os.walk(temp_backend_dir)])
        print(f"Found {total_files} files to upload...")
        print()
        
        # Upload all files from the backend directory to the Space
        uploaded_count = 0
        for root, dirs, files in os.walk(temp_backend_dir):
            for file in files:
                local_file_path = os.path.join(root, file)
                
                # Calculate the relative path from the backend directory
                relative_file_path = os.path.relpath(local_file_path, temp_backend_dir)
                
                # Skip cache directories and test databases
                if ("__pycache__" in local_file_path or 
                    ".pytest_cache" in local_file_path or 
                    "todo_test.db" in local_file_path or
                    ".git" in local_file_path):
                    continue
                
                # Upload the file to the Space
                print(f"Uploading {relative_file_path}...")
                api.upload_file(
                    path_or_fileobj=local_file_path,
                    path_in_repo=relative_file_path,
                    repo_id=repo_id,
                    repo_type="space"
                )
                uploaded_count += 1
        
        print()
        print(f"✓ Successfully uploaded {uploaded_count} files to https://waseem4100-todoapi2.hf.space!")
        print("Your backend should now be deployed on the Hugging Face Space.")

except Exception as e:
    print(f"✗ Error during upload: {str(e)}")
    exit(1)