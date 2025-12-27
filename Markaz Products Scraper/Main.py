from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set Chrome options to ignore SSL errors
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=chrome_options)  # Ensure ChromeDriver is installed

base_url = "https://www.shop.markaz.app/explore/supplier/605"

try:
    for page in range(1, 4):
        driver.get(base_url)
        # Increase wait time and adjust selector
        try:
            WebDriverWait(driver, 15).until(  # Increased to 15 seconds
                EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item"))  # Adjust to actual class
            )
            products = driver.find_elements(By.CLASS_NAME, "product-item")  # Adjust to actual class
            if not products:
                print(f"No products found on page {page}. Check selectors.")
            for product in products:
                try:
                    title = product.find_element(By.CLASS_NAME, "title").text  # Adjust to actual class
                    price = product.find_element(By.CLASS_NAME, "price").text  # Adjust to actual class
                    print(f"Title: {title}, Price: {price}")
                except Exception as e:
                    print(f"Could not extract data from a product on page {page}: {e}")
        except Exception as e:
            print(f"Timeout or error on page {page}: {e}")
        time.sleep(2)
except Exception as e:
    print(f"Main error: {e}")
finally:
    driver.quit()