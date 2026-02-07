# Deploy Todo App: Backend on Hugging Face, Frontend on Vercel

## Overview
This guide will help you deploy the backend to Hugging Face Spaces and the frontend to Vercel, then connect them together.

## Part 1: Deploy Backend to Hugging Face Spaces

### Step 1: Prepare your backend for Hugging Face
1. Create a new folder called `hf-backend` in your project root
2. Copy all backend files to this folder
3. Create the following files in the `hf-backend` directory:

**Dockerfile:**
```Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Run the application with uvicorn on port 7860
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

**app.py (Hugging Face compatible entrypoint):**
```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import auth, todos
from sqlmodel import SQLModel
from src.database.database import engine
from src.models.user import User
from src.models.todo import Todo

# Initialize FastAPI app
app = FastAPI(title="Todo Management API", version="1.0.0")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This should be set to your Vercel frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(todos.router, prefix="/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Todo Management API running on Hugging Face Spaces"}

@app.on_event("startup")
def on_startup():
    # Create database tables
    SQLModel.metadata.create_all(bind=engine)

from fastapi.responses import JSONResponse

# Error handling
@app.exception_handler(404)
async def not_found_error(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Resource not found"})

@app.exception_handler(500)
async def internal_error(request, exc):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.exception_handler(TypeError)
async def type_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": f"Type error: {str(exc)}"})

# Simple function to serve as the main entry point for Hugging Face
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
```

**requirements.txt:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlmodel==0.0.16
psycopg2-binary==2.9.11
alembic==1.13.1
python-multipart==0.0.6
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
pydantic[email]==2.5.0
uuid==1.30
python-dotenv==1.0.0
```

**README.md for the Space:**
```
---
title: Todo Management API
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# Todo Management API

A FastAPI-based todo management backend deployed on Hugging Face Spaces.

## API Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /todos` - Get all user's todos
- `POST /todos` - Create a new todo
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a specific todo
- `DELETE /tos/{id}` - Delete a specific todo
- `PATCH /todos/{id}/toggle-complete` - Toggle todo completion status

## Environment Variables

Set these in your Space settings:
- `DATABASE_URL`: PostgreSQL database URL
- `SECRET_KEY`: Secret key for JWT tokens
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Note

This backend is designed to work with the Todo frontend deployed separately.
```

### Step 2: Create Hugging Face Space
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - SDK: Docker
   - License: MIT (or your preference)
   - Hardware: CPU (Free tier)
   - Visibility: Public or Private
4. For repository, choose "Upload files"
5. Upload all files from your `hf-backend` folder

### Step 3: Configure Environment Variables
1. In your Space dashboard, go to "Settings"
2. Under "Secrets", add:
   - DATABASE_URL: Your PostgreSQL database connection string
   - SECRET_KEY: A long random secret key for JWT tokens
   - ALGORITHM: HS256
   - ACCESS_TOKEN_EXPIRE_MINUTES: 30 (or your preference)

### Step 4: Run Database Migrations
After the Space builds and deploys, you'll need to run the database migrations:
1. Go to your Space URL
2. The application should start automatically
3. You may need to access the Space's terminal to run:
   ```bash
   alembic upgrade head
   ```

## Part 2: Deploy Frontend to Vercel

### Step 1: Prepare for Vercel deployment
The frontend should already be ready for Vercel deployment. Ensure you have:
- `vercel.json` in the frontend directory (already exists)
- `package.json` with all dependencies (already exists)

### Step 2: Deploy to Vercel
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Vercel CLI if you haven't already:
   ```bash
   npm install -g vercel
   ```

3. Login to Vercel:
   ```bash
   vercel login
   ```

4. Deploy the frontend:
   ```bash
   vercel --prod
   ```

5. When prompted for environment variables, set:
   - `NEXT_PUBLIC_API_BASE_URL`: Use your Hugging Face Space URL (e.g., `https://your-username-todo-backend.hf.space`)

## Part 3: Connect Backend and Frontend

The connection happens automatically when you set the `NEXT_PUBLIC_API_BASE_URL` environment variable in Vercel to point to your Hugging Face Space backend URL.

## Verification

1. Visit your Vercel frontend URL
2. Register a new account
3. Create a new todo
4. Verify that the todo is saved and retrieved from the backend
5. Test all functionality (create, update, delete, toggle completion)

## Important Notes

- Hugging Face Spaces may have slower cold starts - the first API call after inactivity may take longer
- Make sure your CORS settings in the backend allow requests from your Vercel frontend URL
- Monitor your Space usage as free tier has limitations
- Database migrations need to be run after initial deployment

## Troubleshooting

- **Backend not connecting to frontend**: Check that `NEXT_PUBLIC_API_BASE_URL` is set correctly in Vercel
- **Database connection errors**: Verify your `DATABASE_URL` in Hugging Face Space settings
- **CORS errors**: The backend currently allows all origins, but you can restrict this in production
- **Slow response times**: This is typical for free Hugging Face Spaces due to cold starts
- **Space sleeping**: Free Spaces sleep after 48 hours of inactivity - first request will wake it up