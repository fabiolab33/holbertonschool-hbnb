from dotenv import load_dotenv
import os

# CRITICAL: Load .env BEFORE importing app
load_dotenv()

# Verify environment loaded
print(f"🔧 Environment: USE_DATABASE = {os.getenv('USE_DATABASE')}")

from app import create_app

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"\n{'='*60}")
    print(f"Starting HBnB API in {config_name.upper()} mode")
    print(f"Server running on http://{host}:{port}")
    print(f"API Documentation: http://{host}:{port}/api/docs")
    print(f"{'='*60}\n")
    
    app.run(host=host, port=port, debug=app.config['DEBUG'])
