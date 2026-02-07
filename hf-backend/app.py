import sys
import os

# Print debugging information
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# List all files in the current directory
print("Files in current directory:")
for item in os.listdir('.'):
    print(f"  - {item}")
    if os.path.isdir(item):
        print(f"    [DIR]")
        try:
            for sub_item in os.listdir(item):
                print(f"      - {sub_item}")
                if os.path.isdir(f"{item}/{sub_item}"):
                    print(f"        [DIR]")
                    try:
                        for sub_sub_item in os.listdir(f"{item}/{sub_item}"):
                            print(f"          - {sub_sub_item}")
                    except:
                        pass
        except:
            pass

# Try to determine the actual structure and adapt accordingly
import fastapi
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Todo Management API", version="1.0.0")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create placeholder routers in case the imports fail
auth_router = APIRouter()
todos_router = APIRouter()

# Add placeholder endpoints
@auth_router.get("/")
def auth_placeholder():
    return {"status": "auth service", "location": "trying to locate src/api/routes/auth.py"}

@todos_router.get("/")
def todos_placeholder():
    return {"status": "todos service", "location": "trying to locate src/api/routes/todos.py"}

# Add the routers to the main app
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(todos_router, prefix="/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {
        "message": "Todo Management API - Checking directory structure",
        "working_dir": os.getcwd(),
        "files": os.listdir('.')
    }

# Try to dynamically locate and import modules
def dynamic_import_check():
    """Function to dynamically check and import modules"""
    import importlib.util
    
    # Look for the actual location of the route files
    possible_paths = [
        './src/api/routes/auth.py',
        './api/routes/auth.py', 
        './routes/auth.py',
        './src/routes/auth.py',
        './backend/src/api/routes/auth.py'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found auth.py at: {path}")
            # Try to import using importlib
            try:
                spec = importlib.util.spec_from_file_location("auth", path)
                auth_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(auth_module)
                
                # Check if router exists in the module
                if hasattr(auth_module, 'router'):
                    print("Successfully loaded auth router")
                    return True
            except Exception as e:
                print(f"Error loading from {path}: {e}")
    
    print("Could not find auth.py in expected locations")
    return False

# Run the check
dynamic_import_check()

if __name__ == "__main__":
    import uvicorn
    import logging
    logging.basicConfig(level=logging.INFO)
    
    port = int(os.getenv("PORT", 7860))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)