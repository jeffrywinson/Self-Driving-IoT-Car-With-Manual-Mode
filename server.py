# server.py

import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows the website to connect to the server

DATA_FILE = "sensor_data.txt"

@app.route('/sensor_data')
def get_sensor_data():
    """Reads sensor data from the file and returns it as JSON."""
    data = {}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                for line in f:
                    key, value = line.strip().split(":")
                    # Ensure values are converted to the correct type
                    data[key] = float(value) if '.' in value else int(value)
        except Exception as e:
            return jsonify({"error": f"Failed to read file: {str(e)}"}), 500
    return jsonify(data)

@app.route('/')
def serve_index():
    """Serves the index.html file."""
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    # You will run this file on your computer
    app.run(host='0.0.0.0', port=5000)