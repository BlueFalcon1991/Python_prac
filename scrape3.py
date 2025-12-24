
import requests
from bs4 import BeautifulSoup

# 1. Fetch the Markets landing page
url = "https://economictimes.indiatimes.com/markets"
headers = {"User-Agent": "Scraping101 (+your_email@example.com)"}

resp = requests.get(url, headers=headers, timeout=20)
print("Status:", resp.status_code)

# 2. Parse the HTML
soup = BeautifulSoup(resp.text, "html.parser")

# 3. Find the Sensex and Nifty sections by ID (replace with actual IDs)
sensex_tag = soup.find_all("span",class_="h1")
nifty_tag = soup.find(id="Nifty")

# 4. Extract text safely
sensex = sensex_tag.get_text(strip=True) if sensex_tag else "N/A"
nifty = nifty_tag.get_text(strip=True) if nifty_tag else "N/A"

print("Sensex:", sensex)
print("Nifty:", nifty)