# part2/run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Run the app in debug mode for development purposes
    app.run(host="0.0.0.0", port=5000, debug=True)
