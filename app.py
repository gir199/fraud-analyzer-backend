from flask import Flask, jsonify, request # Import request
from flask_cors import CORS
import pandas as pd
import os
import google.generativeai as genai # Import the Gemini library

# --- SETUP ---
app = Flask(__name__)
CORS(app)
# Configure Gemini from the environment variable on Render
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# --- API ENDPOINTS ---
@app.route("/")
def read_root():
    return jsonify(message="Fraud Analyzer API is running.")

@app.route("/debarred-entities", methods=['GET'])
def get_debarred_entities():
    # ... (your existing code for this endpoint) ...
    file_path = 'debarred_entities.csv'
    if not os.path.exists(file_path):
        return jsonify(error="Data file not found."), 404
    df = pd.read_csv(file_path)
    return jsonify(df.to_dict(orient='records'))

@app.route("/analyze-tip", methods=['POST'])
def analyze_tip():
    """
    Receives text from the app and uses Gemini to analyze it for fraud.
    """
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify(error="No text provided for analysis."), 400

    tip_text = data['text']
    prompt = f"Analyze the following stock tip for signs of financial fraud. List the specific red flags. Tip: '{tip_text}'"

    try:
        response = model.generate_content(prompt)
        return jsonify(analysis=response.text)
    except Exception as e:
        return jsonify(error=str(e)), 500
