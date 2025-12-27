# import requests
# import csv
# import time

# headers = {
#     "User-Agent": "Mozilla/5.0"
# }

# # Confirmed working API
# API_URL = "https://api.markaz.app/api/product/get-products-by-supplier-id?page={}&supplierId=605&limit=24"

# all_products = []

# for page in range(1, 100):  # adjust max page count as needed
#     print(f"📦 Scraping page {page}")
#     url = API_URL.format(page)
#     response = requests.get(url, headers=headers)

#     if response.status_code != 200:
#         print(f"❌ Failed to fetch page {page}")
#         break

#     data = response.json()
#     products = data.get("products", [])

#     if not products:
#         print("✅ No more products found. Stopping.")
#         break

#     for p in products:
#         all_products.append({
#             "Name": p.get("name"),
#             "Price": p.get("price"),
#             "Old Price": p.get("oldPrice"),
#             "Rating": p.get("rating"),
#             "Stock": p.get("stock"),
#             "Image URL": p.get("image"),
#         })

#     time.sleep(1)  # Be polite to server

# # Save to CSV
# with open("markaz_products.csv", "w", newline='', encoding="utf-8") as f:
#     writer = csv.DictWriter(f, fieldnames=all_products[0].keys())
#     writer.writeheader()
#     writer.writerows(all_products)

# print("✅ Done! Data saved to 'markaz_products.csv'")





# import requests
# from bs4 import BeautifulSoup
# import csv
# import time

# base_url = "https://www.shop.markaz.app/explore/supplier/605?page={}"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
# }

# all_products = []

# for page in range(1, 10):  # limit page range for safety
#     print(f"📦 Scraping page {page}")
#     url = base_url.format(page)

#     try:
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             print(f"❌ Failed to fetch page {page}")
#             break

#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Update this selector based on correct HTML structure
#         products = soup.select(".product-card")  
#         if not products:
#             print("✅ No items found on page. Stopping.")
#             break

#         for prod in products:
#             name = prod.select_one(".product-title").get_text(strip=True) if prod.select_one(".product-title") else "N/A"
#             price = prod.select_one(".price").get_text(strip=True) if prod.select_one(".price") else "N/A"

#             all_products.append({
#                 "Name": name,
#                 "Price": price
#             })

#         time.sleep(1)

#     except Exception as e:
#         print(f"❌ Error scraping page {page}: {e}")
#         break

# # Only write CSV if there's something to write
# if all_products:
#     with open("products.csv", "w", newline='', encoding='utf-8') as f:
#         writer = csv.DictWriter(f, fieldnames=all_products[0].keys())
#         writer.writeheader()
#         writer.writerows(all_products)
#     print("✅ Done! Data saved.")
# else:
#     print("⚠️ No data scraped. CSV not created.")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv

# Headless browser optional
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment for headless

# WebDriver setup
service = Service()
driver = webdriver.Chrome(service=service, options=options)

# Target URL (change this to your actual website)
url = ""
driver.get(url)
time.sleep(3)  # Wait for JS content to load

products = []

try:
    page = 1
    while True:
        print(f"📦 Scraping page {page}...")

        items = driver.find_elements(By.CSS_SELECTOR, ".product-card")  # Update selector as per your site
        if not items:
            print("⚠️ No items found on this page.")
            break

        for item in items:
            try:
                name = item.find_element(By.CSS_SELECTOR, ".product-name").text.strip()
                price = item.find_element(By.CSS_SELECTOR, ".product-price").text.strip()
                products.append([name, price])
            except Exception as e:
                print("❌ Error in item parsing:", e)

        # Check if there's a next page button
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            if "disabled" in next_button.get_attribute("class"):
                break
            else:
                next_button.click()
                time.sleep(2)
                page += 1
        except:
            print("🚫 No next page found.")
            break

finally:
    driver.quit()

# Save to CSV
if products:
    with open("products.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Price"])
        writer.writerows(products)
    print("✅ CSV saved with", len(products), "products.")
else:
    print("⚠️ No data scraped. CSV not created.")
