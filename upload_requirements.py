#!/usr/bin/env python3
"""
Script to upload updated requirements.txt to Hugging Face Space
"""
import os
from pathlib import Path
from huggingface_hub import upload_file

SPACE_ID = "Waseem4100/todoapp"

def upload_requirements():
    """Upload the updated requirements.txt file to the Hugging Face Space"""

    # Set the token as an environment variable
    # NOTE: This is a placeholder token - replace with your actual token when running locally
    hf_token = "YOUR_HF_TOKEN_HERE"

    file_path = Path("hf-backend") / "requirements.txt"
    if file_path.exists():
        print(f"Uploading updated requirements.txt to {SPACE_ID}...")
        upload_file(
            path_or_fileobj=str(file_path),
            path_in_repo="requirements.txt",
            repo_id=SPACE_ID,
            repo_type="space",
            token=hf_token,
            commit_message="Update requirements.txt to include PyJWT"
        )
        print("[SUCCESS] Uploaded updated requirements.txt")
    else:
        print("⚠ requirements.txt not found!")

if __name__ == "__main__":
    upload_requirements()