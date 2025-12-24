import requests
import mysql.connector
import requests
from bs4 import BeautifulSoup

url =  'https://webscraper.io/test-sites'
headers = {"User-Agent": "Scraping101 (+your_email@example.com)"}
resp = requests.get(url, headers=headers, timeout=20)
print("Status:", resp.status_code)
# print("First 200 chars:")
# print(resp.text[:200])
soup = BeautifulSoup(resp.text, 'html.parser')
records={}

for q in soup.select("div.col-lg-7.order-lg-2"): 
    
    link = q.select_one("a")
    desc_tag = q.select_one("p")

    link_url= link.get("href") if link else ""
    link_text=link.get_text(strip=True) if link else ""
    desc = desc_tag.get_text(strip=True) if desc_tag else ""

    if link_text:
        records[link_text] = {"url": link_url, "description": desc}
print(records)

# --- Step 2: Connect to MySQL ---
conn = mysql.connector.connect(
    host="localhost",       # your MySQL server host
    user="root",            # your MySQL username
    password="asd123456", # your MySQL password
    database="wf"       # your database name (make sure it exists)
)
cursor = conn.cursor()
# --- Step 3: Create table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS scraped_sites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    link_text VARCHAR(255),
    url TEXT,
    description TEXT
)
""")
# --- Step 4: Insert data ---
for text, info in records.items():
    cursor.execute("""
        INSERT INTO scraped_sites (link_text, url, description)
        VALUES (%s, %s, %s)
    """, (text, info["url"], info["description"]))

conn.commit()
conn.close()

print("Data inserted successfully into MySQL table.")
