import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- ADD THIS LINE
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# Initialize the Flask application
app = Flask(__name__)
CORS(app) # <-- AND ADD THIS LINE

# ... (the rest of your code remains exactly the same) ...