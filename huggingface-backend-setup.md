# Hugging Face Space Configuration for Todo Backend

## Dockerfile for Hugging Face Space
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

## app.py (for Gradio wrapper - required by Hugging Face Spaces)
```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import auth, todos
from sqlmodel import SQLModel
from src.database.database import engine
from src.models.user import User
from src.models.todo import Todo
from gradio.helpers import create_examples

# Initialize FastAPI app
app = FastAPI(title="Todo Management API", version="1.0.0")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
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
    return JSONResponse(status_code=500, content={"detail": f"Type error: {str(exc)"})

# Gradio interface for Hugging Face Spaces compatibility
import gradio as gr

def run_backend():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

# Create a simple Gradio interface to satisfy Hugging Face Spaces
with gr.Blocks() as demo:
    gr.Markdown("# Todo Management API")
    gr.Markdown("Backend API running on Hugging Face Spaces")
    gr.Markdown(f"API endpoints available at: `/todos` and `/auth`")

# Mount the FastAPI app to the Gradio interface
demo.launch(share=False, server_name="0.0.0.0", server_port=7860, show_api=False)
```

## README.md for Hugging Face Space
```markdown
---
title: Todo Management API
emoji: 🚀
colorFrom: blue
colorTo: yellow
sdk: docker
pinned: false
license: mit
---

# Todo Management API

This is a FastAPI-based todo management backend deployed on Hugging Face Spaces.

## API Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /todos` - Get all user's todos
- `POST /todos` - Create a new todo
- `GET /todos/{id}` - Get a specific todo
- `PUT /todos/{id}` - Update a specific todo
- `DELETE /todos/{id}` - Delete a specific todo
- `PATCH /todos/{id}/toggle-complete` - Toggle todo completion status

## Environment Variables

- `DATABASE_URL`: PostgreSQL database URL
- `SECRET_KEY`: Secret key for JWT tokens
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
```

## requirements.txt (for Hugging Face Space)
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
gradio==4.19.1
```

## Space Configuration Instructions:

1. Create a new Hugging Face Space with Docker SDK
2. Add your backend code to the repository
3. Include the Dockerfile, app.py, README.md, and updated requirements.txt
4. Set environment variables in Space settings:
   - DATABASE_URL: Your PostgreSQL database URL
   - SECRET_KEY: Secret key for JWT tokens
   - ALGORITHM: HS256 (or your preferred algorithm)
   - ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time (e.g., 30)
5. The Space will automatically build and deploy your backend

## Connecting Frontend to Hugging Face Backend:

Once deployed, your Hugging Face Space will have a URL like:
`https://your-username-space-name.hf.space`

Use this URL as the `NEXT_PUBLIC_API_BASE_URL` when deploying to Vercel:
- NEXT_PUBLIC_API_BASE_URL: `https://your-username-space-name.hf.space`

## Important Notes:

- Hugging Face Spaces may have slower cold starts
- Free tier has usage limits
- The backend will be accessible at the Space URL
- Make sure to run database migrations after deployment
- You may need to trigger the first API call to "wake up" the space
```