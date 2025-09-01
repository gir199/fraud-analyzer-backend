import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL for SEBI's debarred entities list
url = "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doUnreg=yes"

# Fetch the page content
response = requests.get(url)

# Parse the HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table (you'll need to inspect the page's HTML to find the right tag)
table = soup.find('table', {'class': 'table-responsive'})

# Use pandas to read the HTML table directly into a DataFrame
df = pd.read_html(str(table))[0]

# Save the data to a CSV file
df.to_csv('debarred_entities.csv', index=False)

print("Scraping complete. Data saved to debarred_entities.csv")