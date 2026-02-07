import sys
import os
# Add the parent directory to the Python path to allow relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.auth import router as auth_router
from api.routes.todos import router as todos_router
from sqlmodel import SQLModel
from database.database import engine
from models.user import User
from models.todo import Todo

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
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(todos_router, prefix="/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Todo Management API"}

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

# For testing purposes, we'll also add exception handlers for the specific errors we saw
@app.exception_handler(TypeError)
async def type_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": f"Type error: {str(exc)}"})