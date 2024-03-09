import re
import json
import datetime
import logging
from zoneinfo import ZoneInfo
import html
import requests
from db import get_db_conn
from geopy.geocoders import Nominatim
import time

# test(Selenium)(显示所有产品信息)(scrape1000個)
# Part 2: Scraping the detail page
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_load_more_button(driver):
    try:
        load_more_button = driver.find_element(By.CSS_SELECTOR, "button.js-load-more")
        driver.execute_script("arguments[0].click();", load_more_button)
        time.sleep(5)  # Wait for new products to load
        return True
    except Exception as e:
        print("Error clicking 'Load More' button:", e)
        return False
    
def get_product_urls_with_selenium(page_url, max_items=1000):
    service = Service(executable_path=r"C:\D\研究所\Q2\TECHIN 510\chromedriver-win64\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get(page_url)
    print(f"Starting scraping on: {driver.current_url}")
    time.sleep(5)  # Wait for the page to load initially

    product_urls = []
    try:
        item_count = 0
        while len(product_urls) < max_items:
            if not click_load_more_button(driver):
                break
                
            print(f"Currently scraping: {driver.current_url}, items loaded: {len(product_urls)}")
                
            # Extract product URLs from the current page
            product_elements = driver.find_elements(By.CSS_SELECTOR, "a.link")
            for elem in product_elements:
                url = elem.get_attribute('href')
                if url.startswith("https://www2.hm.com/en_us/productpage.") and url not in product_urls:
                    product_urls.append(url)
                    item_count += 1
                    if len(product_urls) >= max_items:
                        break
    except Exception as e:
        print("An error occurred during scraping:", e)

    print(f"Reached {len(product_urls)} items, starting to scrape item URLs...")
    driver.quit()
    return product_urls[:max_items]  # Make sure not to return more than max_items


def scrape_product_info(driver, url, product_dict):
    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        product_name_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#js-product-name > div > h1"))
        )
        product_name = product_name_element.text.strip()
        
        product_price_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#product-price > div > span"))
        )
        product_price = product_price_element.text.strip()
        
        product_colors_elements = WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#main-content > div.product.parbase > div.layout.pdp-wrapper.product-detail.sticky-footer-wrapper.js-reviews > div.module.product-description.sticky-wrapper.pdp-container > div.column2 > div > div > div.product-colors.miniatures.clearfix.slider-completed.loaded > h3"))
        )
        product_colors = [color_element.text.strip() for color_element in product_colors_elements]
        
        # Check if the product with the same name and price exists in the dictionary
        key = (product_name, product_price)
        if key in product_dict:
            product_dict[key]['product_colors'].extend(product_colors)
        else:
            product_dict[key] = {
                'product_name': product_name,
                'product_price': product_price,
                'product_colors': product_colors
            }
        
    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")

    
base_url = "https://www2.hm.com/en_us/women/products/view-all.html"
product_urls = get_product_urls_with_selenium(base_url, 1000)

print(f"Total products scraped: {len(product_urls)}")

# Dictionary to store products based on name and price
product_dict = {}

# Reuse the same webdriver instance for efficiency
service = Service(executable_path=r"C:\D\研究所\Q2\TECHIN 510\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Scrape product info for all URLs
for idx, url in enumerate(product_urls, start=1):
    print(f"Scraping URL {idx}/{len(product_urls)}: {url}")
    scrape_product_info(driver, url, product_dict)
    
driver.quit()

# Print the scraped products
print("Scraped Product Information:")
for idx, (key, product_info) in enumerate(product_dict.items(), start=1):
    print(f"Product {idx}:")
    print("Product Name:", product_info['product_name'])
    print("Product Price:", product_info['product_price'])
    print("Product Colors:", product_info['product_colors'])
    print("-" * 50)