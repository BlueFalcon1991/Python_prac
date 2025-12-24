import re
import requests
from bs4 import BeautifulSoup
import mysql.connector
from urllib.parse import urljoin, urlparse

BASE = "https://webscraper.io"
START = f"{BASE}/test-sites"
HEADERS = {"User-Agent": "Scraping101 (+your_email@example.com)"}

# ---------- MySQL setup ----------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="asd123456",
    database="wf"
)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS scrape_test2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section_name VARCHAR(255),
    section_url TEXT,
    prod_name TEXT,
    prod_desc TEXT,
    prod_price VARCHAR(50)
)
""")
conn.commit()

def get_soup(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def unique_abs_links(soup, base_url, prefix_filter=None):
    out = set()
    for a in soup.select('a[href]'):
        href = a['href'].strip()
        absu = urljoin(base_url, href)
        if prefix_filter and not absu.startswith(prefix_filter):
            continue
        # same host only
        if urlparse(absu).netloc == urlparse(BASE).netloc:
            out.add(absu)
    return out

def page_has_products(soup):
    # Robust: accept either Bootstrap "thumbnail" or newer "card" containers,
    # but only if they contain an a.title (the actual product title).
    cards = []
    for box in soup.select("div.card, div.thumbnail"):
        if box.select_one("a.title"):
            cards.append(box)
    return cards

# ---------- 1) collect top-level e-commerce test sites ----------
home = get_soup(START)
section_links = []  # (section_name, section_url)
for h2 in home.select("h2, h3, h4"):  # headings contain the section links
    a = h2.find("a", href=True)
    if a and a['href'].startswith("/test-sites/e-commerce/"):
        section_name = a.get_text(strip=True)
        section_url = urljoin(BASE, a['href'])
        section_links.append((section_name, section_url))

# Fallback: if headings didn’t catch them, sweep all anchors:
if not section_links:
    for a in home.select('a[href^="/test-sites/e-commerce/"]'):
        section_links.append((a.get_text(strip=True) or "E-commerce site", urljoin(BASE, a['href'])))

# Deduplicate by URL
seen = set()
section_links = [(n,u) for n,u in section_links if not (u in seen or seen.add(u))]

# ---------- 2) for each section, drill to leaf listing pages ----------
visited = set()
for section_name, section_url in section_links:
    try:
        section_soup = get_soup(section_url)
    except Exception as e:
        print(f"Skip {section_url}: {e}")
        continue

    # BFS-ish crawl limited to this section path, depth <= 2
    q = [section_url]
    depth = {section_url: 0}
    leaf_pages = []

    while q:
        url = q.pop(0)
        if url in visited: 
            continue
        visited.add(url)

        try:
            soup = get_soup(url)
        except Exception as e:
            print(f"Skip {url}: {e}")
            continue

        cards = page_has_products(soup)
        if cards:
            leaf_pages.append((url, cards))
            continue  # don’t go deeper once we found products on this page

        if depth[url] >= 2:
            continue  # keep crawl shallow to avoid wandering

        # Enqueue deeper links under the same e-commerce section (e.g., /allinone/..., /static/...)
        # Skip product detail pages (/product/...)
        for absu in unique_abs_links(soup, url, prefix_filter=section_url.rsplit('/', 1)[0]):
            if "/product/" in absu:
                continue
            # stay within the same test site family (e.g., allinone)
            if not absu.startswith(section_url):
                continue
            if absu not in visited and absu not in depth:
                depth[absu] = depth[url] + 1
                q.append(absu)

    # ---------- 3) extract products from each leaf page ----------
    for leaf_url, cards in leaf_pages:
        for box in cards:
            # Name
            a = box.select_one("a.title")
            if not a:
                continue
            prod_name = a.get_text(strip=True)

            # Price (h4.price is common; fall back to any heading with a $-like number)
            price_tag = box.select_one("h4.price")
            if price_tag:
                prod_price = price_tag.get_text(strip=True)
            else:
                # fallback regex search in the box text
                m = re.search(r'[$€£]\s*\d[\d\.,]*', box.get_text(" ", strip=True))
                prod_price = m.group(0) if m else ""

            # Description
            desc_tag = box.select_one("p.description") or box.find("p")
            prod_desc = desc_tag.get_text(strip=True) if desc_tag else ""

            # Insert row with earlier columns + product fields
            cur.execute(
                """INSERT INTO scrape_test2 (section_name, section_url, prod_name, prod_desc, prod_price)
                   VALUES (%s, %s, %s, %s, %s)""",
                (section_name, leaf_url, prod_name, prod_desc, prod_price)
            )
    conn.commit()

cur.close()
conn.close()
print("Done.")
