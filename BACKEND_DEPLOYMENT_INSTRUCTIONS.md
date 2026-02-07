# Todo App Backend Deployment to Hugging Face Spaces

This document explains how to deploy the Todo App backend to your Hugging Face Space at https://waseem4100-todoapi2.hf.space

## Prerequisites

1. A Hugging Face account
2. A valid access token with write permissions
3. The backend code has been fixed to resolve deployment issues

## Fixed Issue

The backend had a deployment error due to an unsupported parameter in SQLModel:
- **Issue**: `Field(foreign_key="user.id", ondelete="CASCADE")` caused TypeError
- **Fix**: Changed to `Field(foreign_key="user.id")` (removed unsupported `ondelete` parameter)

## Deployment Methods

### Method 1: Using Environment Variable (Recommended)

1. Get your Hugging Face token:
   - Go to https://huggingface.co/settings/tokens
   - Click on 'New token'
   - Give it a name (e.g., 'todo-api-upload')
   - Select 'Write' role for uploading files
   - Copy the generated token

2. Set the environment variable:
   ```bash
   # On Windows Command Prompt:
   set HF_TOKEN=your_token_here
   
   # On Windows PowerShell:
   $env:HF_TOKEN="your_token_here"
   ```

3. Run the upload script:
   ```bash
   python upload_backend_with_env.py
   ```

### Method 2: Using Hugging Face CLI

1. Install the Hugging Face CLI if not already installed:
   ```bash
   pip install huggingface_hub
   ```

2. Authenticate:
   ```bash
   huggingface-cli login
   ```
   Enter your token when prompted.

3. Upload the files:
   ```bash
   huggingface-cli upload Waseem4100/todoAPI2 D:\Coding\hackathons\todo-app\backend . --repo-type space
   ```

## Files Included in Deployment

The following files from the backend directory will be uploaded:
- main.py (entry point)
- src/ directory (all source code)
- requirements.txt (dependencies)
- Dockerfile (container configuration)
- Procfile (process types)
- alembic/ directory (database migrations)
- alembic.ini (migration configuration)
- runtime.txt (Python version specification)

## Post-Deployment

After successful upload:
1. The Hugging Face Space will automatically rebuild
2. Your API will be accessible at https://waseem4100-todoapi2.hf.space
3. The API endpoints will be available as defined in the backend code

## Troubleshooting

If you encounter issues:
1. Verify your token has write permissions
2. Check that the repository name matches your Space name
3. Ensure all required files are present in the backend directory
4. Check the Space logs for specific error messages