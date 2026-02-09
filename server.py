from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import os
import sys

app = Flask(__name__)

# Configure CORS
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*")
if allowed_origins != "*":
    allowed_origins = allowed_origins.split(",")

CORS(app, origins=allowed_origins)

@app.route('/refresh', methods=['POST'])
def refresh_data():
    try:
        # Define the command
        command = [
            sys.executable, 
            'execution/fetch_reddit_posts.py', 
            '--subreddits', 'n8n', 'automation', 
            '--limit', '100', 
            '--top', '5', 
            '--output', 'reddit-viewer/public/data.json'
        ]
        
        # Execute the fetch script
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return jsonify({"status": "success", "message": "Data refreshed successfully"}), 200
        
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error", 
            "message": "Script execution failed", 
            "output": e.stdout, 
            "error_output": e.stderr
        }), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Flask server on port {port}...")
    app.run(port=port)
