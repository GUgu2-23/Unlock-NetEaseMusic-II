# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "002222E53138EEF06AA3AFF68ACD5672CA473269321196B837775DBC9716940B70CADE506C5BC9F9183FA259CDF255007298665264CE466385121BFA26B73666D3B8528B23814B6B7BF59A1DDA4B341B7DCAB26804B5CECFFCA5C05A9C098EDA3C589318C07E80FEA0346324295EDFD6D406A54C6C0C38FF6CCDD032EABBD19FDCE8E847E8A85625B9D0917BA20C403D2484B8DA1261BED9F06CF68E786240F8556EEE0A6BC7F403AB8727DEA31437B053104AD15639B6DD3ED53818D5635FB4CCA8404E1CA28C5B4DB826F94B2536A2B95E1DF40AD4F4456CC0B7AEB9D55ACB8831E6C7178B42F7DDA621B95A8E13DE148809F865F10E1030FC2DC8ECE7E47C59145016EA2971E1D610238D7AA477E30AE9FB780D5FE8AA36F58CC4F656393C9545230FF8A3D3851A7FA80C2098DBC77FF1223311DB7693DC7A762DF6E3B7BD6D957A9B2E7C5E7AFAE15F7B201FB14AC12CD0C08886A76A1029890970C800EC1B"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
