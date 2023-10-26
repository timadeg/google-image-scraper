import os
import time
import requests
import argparse
import logging
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IMAGE_SAVE_PATH = os.path.join('.', 'images')
os.makedirs(IMAGE_SAVE_PATH, exist_ok=True)

def setup_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def click_consent_if_exists(driver):
    try:
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 'your_xpath_here'))
        )
        consent_button.click()
    except TimeoutException:
        logger.info("No consent form found, proceeding...")

def download_image(query, num_images, start_index=0):
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    driver = setup_driver()

    try:
        driver.get(url)
        click_consent_if_exists(driver)

        for _ in range(15):  
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)

        action_chains = ActionChains(driver)

        for i in range(start_index, start_index + num_images):
            try:
                image_thumbnail = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.rg_i"))
                )[i]
                action_chains.move_to_element(image_thumbnail).click().perform()
                time.sleep(2)

                img_tag = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.pT0Scc.iPVvYb"))
                )
                img_link = img_tag.get_attribute("src")

                if img_link is not None and img_link.startswith('http'):
                    response = requests.get(img_link)
                    image_bytes = BytesIO(response.content)
                    img = Image.open(image_bytes)
                    img_filename = f"{os.path.join(IMAGE_SAVE_PATH, query.replace(' ', '_'))}_{i}.png"
                    img.save(img_filename)
                    print(f"{query} - Downloaded image: {i}")
                else:
                    print(f"Couldn't download image for: {query}. Error: Link is None or not http")

            except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException, Exception) as e:
                print(f"Error occurred for {query}: {str(e)}")

    finally:
        driver.quit()


def main():
    parser = argparse.ArgumentParser(description="Google Image Scraper")
    parser.add_argument("query", type=str, help="Search term for images")
    parser.add_argument("num_images", type=int, help="Number of images to download")
    parser.add_argument("--start_index", type=int, default=0, help="Starting index for images")

    args = parser.parse_args()

    download_image(args.query, args.num_images, args.start_index)

if __name__ == "__main__":
    main()
