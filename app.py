from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup

# Create the Flask web server application
app = Flask(__name__)
CORS(app)

# --- SCRAPING FUNCTION ---
def scrape_debarred_entities():
    """Scrapes SEBI's debarred list and saves it to a CSV file."""
    print("Starting the scraping process...")
    url = "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doUnreg=yes"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'table-responsive'})
    
    if table:
        df = pd.read_html(str(table))[0]
        df.to_csv('debarred_entities.csv', index=False)
        print("Scraping complete. Data saved to debarred_entities.csv")
    else:
        print("Error: Could not find the data table on the page.")

# --- API ENDPOINTS ---
@app.route("/")
def read_root():
    return jsonify(message="Fraud Analyzer API is running.")

@app.route("/debarred-entities", methods=['GET'])
def get_debarred_entities():
    """Reads the CSV file and returns its content as JSON."""
    file_path = 'debarred_entities.csv'
    if not os.path.exists(file_path):
        return jsonify(error="Data file not found."), 404
        
    df = pd.read_csv(file_path)
    return jsonify(df.to_dict(orient='records'))

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    # When this script is run directly (like by the GitHub Action),
    # it will just run the scraper.
    scrape_debarred_entities()
    
    # To run the web server for local testing, you would comment out the line above
    # and uncomment the line below:
    # app.run(debug=True, port=8080)
