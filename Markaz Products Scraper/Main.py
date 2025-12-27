import requests
from bs4 import BeautifulSoup
import time
import csv

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

BASE_URL = ""
START_URL = ""

def get_soup(url):
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")

def parse_product_detail(url):
    soup = get_soup(BASE_URL + url)
    title = soup.select_one("h1.product-title").get_text(strip=True)
    price = soup.select_one(".product-price").get_text(strip=True)
    img = soup.select_one(".product-image img")["src"]
    desc = soup.select_one(".product-description").get_text(strip=True)
    return {"title": title, "price": price, "image": img, "description": desc, "url": BASE_URL+url}

def scrape_supplier():
    page = 1
    all_products = []

    while True:
        page_url = f"{START_URL}?page={page}"
        soup = get_soup(page_url)
        items = soup.select(".product-card a")  # adjust selector as needed

        if not items:
            break

        for a in items:
            link = a["href"]
            try:
                data = parse_product_detail(link)
                all_products.append(data)
                time.sleep(0.5)  # polite scraping
            except Exception as e:
                print(f"Error scraping {link}: {e}")

        page += 1

    return all_products

if __name__ == "__main__":
    products = scrape_supplier()
    with open("markaz_products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
    print(f"Scraped {len(products)} products ✅")
