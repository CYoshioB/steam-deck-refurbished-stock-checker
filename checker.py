from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from env import DISCORD_WEBHOOK_URL

# Configurations
webhook_url = DISCORD_WEBHOOK_URL
page_url = "https://store.steampowered.com/sale/steamdeckrefurbished/"
product_titles = [
    # Comment out the SKUs you don't wish to check for
    "Steam Deck 512GB OLED - Valve Certified Refurbished",
    "Steam Deck 1TB OLED - Valve Certified Refurbished",
    "Steam Deck 64GB LCD - Valve Certified Refurbished",
    "Steam Deck 256GB LCD - Valve Certified Refurbished",
    "Steam Deck 512GB LCD - Valve Certified Refurbished",
]
debug = False # Set to True to always send a notification with a screenshot

# Set up Selenium Firefox WebDriver options
options = Options()
options.add_argument('-headless')
options.add_argument('-no-sandbox')
options.add_argument('-disable-dev-shm-usage')
service = Service()

# Start WebDriver
driver = webdriver.Firefox(service=service, options=options)
waitTime = 5    # Allow page to load in its entirety

try:
    driver.get(page_url)

    # Wait for page to load dynamic content
    WebDriverWait(driver, waitTime).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(waitTime)  # Extra wait to ensure all dynamic content is fully loaded

    # Set the window size to capture the full page
    driver.set_window_size(1920, 1500)
    '''
    # Original Full Page Method
    # Check for "Out of stock" occurrences
    page_source = driver.page_source
    add_to_cart_count = page_source.lower().count("add to cart")
    '''
    # Updated per-SKU Method
    product_found = False
    for title in product_titles:
        try:
            # Check if product is present on webpage
            product_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{title}')]")
            # Locate the product's "Add to Cart" button
            add_to_cart_button = product_element.find_element(By.XPATH, "..//following-sibling::*//*[contains(@class, 'CartBtn')]//span[contains(text(), 'Add to Cart')]")
            # Check if "Add to Cart" is present/usable
            if add_to_cart_button.is_displayed():
                product_found = True
                break
        except Exception as e:
            # If nothing is found or error occurs, move on to next product
            continue
    
    # Take a full-page screenshot
    screenshot_path = "/tmp/steamdeck_stock_status.png"
    driver.save_screenshot(screenshot_path)

    # Determine if a notification should be sent
    if (product_found):                     # add_to_cart_count > 0, for old method
        print("Steam Deck Refurbished SKU(s) is now in stock!")
        message = {
            "content": f":white_check_mark: Steam Deck Refurbished is now in stock!",
        }
        files = {
            "file": ("screenshot.png", open(screenshot_path, "rb"))
        }
        response = requests.post(webhook_url, data=message, files=files)
    elif debug:
        print("Debug test message.")
        message = {
            "content": f":x: Steam Deck Refurbished SKU(s) may or may not be in stock.",
        }
        files = {
            "file": ("screenshot.png", open(screenshot_path, "rb"))
        }
        response = requests.post(webhook_url, data=message, files=files)
    else:
        print("Steam Deck Refurbished SKU(s) is not in stock!\nNo need to notify.")

finally:
    driver.quit()
