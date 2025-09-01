from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

# Create the Flask web server application
app = Flask(__name__)
CORS(app)

# --- API ENDPOINTS ---
# This server's only job is to read the CSV and provide data.

@app.route("/")
def read_root():
    """A default endpoint to check if the API is running."""
    return jsonify(message="Fraud Analyzer API is running.")


@app.route("/debarred-entities", methods=['GET'])
def get_debarred_entities():
    """
    Reads the debarred_entities.csv file created by the GitHub Action
    and returns its content as JSON.
    """
    file_path = 'debarred_entities.csv'
    if not os.path.exists(file_path):
        return jsonify(error="Data file not found. The daily scraper may not have run yet."), 404

    try:
        df = pd.read_csv(file_path)
        records = df.to_dict(orient='records')
        return jsonify(records)
    except Exception as e:
        return jsonify(error=str(e)), 500

# NOTE: The __main__ block for running the scraper is removed.
# The server is started by Gunicorn on Render.
