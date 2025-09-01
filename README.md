# Fraud Analyzer Backend

This project is the backend for a fraud prevention tool. It scrapes public data from SEBI and other sources to identify potential financial scams, verify investment advisors, and analyze suspicious stock tips.

## Features
- Scrapes SEBI's list of registered and debarred entities.
- Designed to be automated using GitHub Actions.
- Provides data to a FlutterFlow frontend application.

## Setup
To run this project locally, you need Python 3.8+.
1. Clone the repository: `git clone https://github.com/gir199/fraud-analyzer-backend.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the script: `python app.py`
