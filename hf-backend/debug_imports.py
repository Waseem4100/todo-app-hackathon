import sys
import os

# Add the current directory to the Python path to allow proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path[:3]}...")  # Print first 3 elements

# Check if src directory exists
src_exists = os.path.exists('./src')
print(f"src directory exists: {src_exists}")

if src_exists:
    # Check if api directory exists
    api_exists = os.path.exists('./src/api')
    print(f"src/api directory exists: {api_exists}")
    
    if api_exists:
        # Check if routes directory exists
        routes_exists = os.path.exists('./src/api/routes')
        print(f"src/api/routes directory exists: {routes_exists}")
        
        if routes_exists:
            # List files in routes directory
            routes_files = os.listdir('./src/api/routes')
            print(f"Files in src/api/routes: {routes_files}")

# Try importing step by step
try:
    import src
    print("Successfully imported src")
except ImportError as e:
    print(f"Failed to import src: {e}")

try:
    import src.api
    print("Successfully imported src.api")
except ImportError as e:
    print(f"Failed to import src.api: {e}")

try:
    import src.api.routes
    print("Successfully imported src.api.routes")
except ImportError as e:
    print(f"Failed to import src.api.routes: {e}")

try:
    from src.api.routes import auth
    print("Successfully imported auth from src.api.routes")
except ImportError as e:
    print(f"Failed to import auth from src.api.routes: {e}")

try:
    from src.api.routes.auth import router
    print("Successfully imported router from src.api.routes.auth")
except ImportError as e:
    print(f"Failed to import router from src.api.routes.auth: {e}")