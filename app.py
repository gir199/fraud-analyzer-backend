import os
import json
from flask import Flask, request, jsonify
import google.generativeai as genai
# You might need to install a library for web scraping, e.g., pip install beautifulsoup4 requests
import requests
from bs4 import BeautifulSoup

# Initialize the Flask application
app = Flask(__name__)

# --- CONFIGURATION ---
# Set your Google AI API key as an environment variable in your terminal
# e.g., export GOOGLE_API_KEY='YOUR_API_KEY_HERE'
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except KeyError:
    print("🔴 Error: GOOGLE_API_KEY environment variable not set.")
    exit()

# --- SIMULATED DATABASE (FOR PROTOTYPE) ---
# For the prototype, we will simulate a database of verified advisors
VERIFIED_ADVISORS = {
    "Rakesh Sharma": "SEBI Registration: SEBI-12345",
    "Priya Singh": "SEBI Registration: SEBI-67890",
    "Anjali Mehta": "SEBI Registration: SEBI-55555"
}

# --- HELPER FUNCTIONS (THE LOGIC) ---

def scan_offer(url):
    """Scrapes a URL, analyzes its text with AI, and returns a formatted string."""
    try:
        # Scrape the webpage text
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = ' '.join(t.get_text() for t in soup.find_all(['p', 'h1', 'h2', 'li']))

        # Build the detailed prompt for the AI
        prompt = f"""
        Analyze the following text from an investment website for signs of fraud.
        Assign a 'riskLevel' of 'Low', 'Medium', or 'High', and provide a brief 'summary'.
        Return the answer ONLY in a valid JSON format with keys "riskLevel" and "summary".

        Text: "{page_text[:4000]}"
        """ # Sliced to stay within token limits

        ai_response = model.generate_content(prompt)
        ai_result_json = json.loads(ai_response.text.strip())
        
        # Format the result into a single string for the UI
        risk = ai_result_json.get('riskLevel', 'Unknown')
        summary = ai_result_json.get('summary', 'No summary available.')
        return f"--- Offer Analysis ---\n\nRisk Level: {risk}\n\nSummary: {summary}"

    except Exception as e:
        return f"--- Error ---\n\nCould not analyze the URL. Reason: {str(e)}"

def check_advisor(name):
    """Checks a name against the simulated database and returns a formatted string."""
    # Check our simple dictionary for the name (case-insensitive check)
    for key, value in VERIFIED_ADVISORS.items():
        if key.lower() == name.lower():
            return f"--- Advisor Check ---\n\nStatus: Verified\n\nName: {key}\nDetails: {value}"
    
    return f"--- Advisor Check ---\n\nStatus: Not Found\n\nDetails: The name '{name}' was not found in the verified registry."


# --- MAIN API ENDPOINT ---
@app.route('/analyze', methods=['POST'])
def analyze_request():
    data = request.get_json()
    if not data or 'userQuery' not in data:
        return jsonify({"resultText": "Error: Invalid request."})

    user_input = data['userQuery'].strip()

    # The "Router" logic to decide which function to call
    if 'http' in user_input or 'www' in user_input:
        result_string = scan_offer(user_input)
    else:
        result_string = check_advisor(user_input)
        
    # Return the final string in a simple JSON object
    return jsonify({"resultText": result_string})

# --- RUN THE SERVER ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)