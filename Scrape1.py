import requests
from bs4 import BeautifulSoup

base_url = "https://webscraper.io"
start_url = f"{base_url}/test-sites"
headers = {"User-Agent": "Scraping101 (+your_email@example.com)"}

# Step 1: Scrape main page
resp = requests.get(start_url, headers=headers, timeout=20)
soup = BeautifulSoup(resp.text, 'html.parser')

records = {}
for q in soup.select("div.col-lg-7.order-lg-2"): 
    link = q.select_one("a")
    desc_tag = q.select_one("p")
    link_url = link.get("href") if link else ""
    link_text = link.get_text(strip=True) if link else ""
    desc = desc_tag.get_text(strip=True) if desc_tag else ""
    if link_text:
        records[link_text] = {
            "url": base_url + link_url,  # Make absolute
            "description": desc
        }
print(records)

# Step 2: Go inside each link
for name, info in records.items():
    print(f"\n--- Inside: {name} ---")
    inner_resp = requests.get(info["url"], headers=headers, timeout=20)
    inner_soup = BeautifulSoup(inner_resp.text, 'html.parser')

    # Example: get all product titles inside this page
    for product in inner_soup.select("div.thumbnail"):
        title = product.select_one("a.title").get_text(strip=True)
        price = product.select_one("h4.price").get_text(strip=True)
        print(f"{title} - {price}")