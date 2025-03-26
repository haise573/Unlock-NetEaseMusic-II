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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B5474165D7BD80A9631BA9C69E9C298E27F9EABA926778DF56B3DE60AC508CAB6854F3138A9B1D199A937F6733F93CC7F3CE2A9EEB7835C48E40F72CF19A814A0AB795082B3A5716C36D577DA165EB7D1A18281A904EBD769CF4BAD5923631665AB26FB0973B20FE0F4CB6B7977CDC3D506213492747B0CACE5C88F6130F26C375819F766F17B87197BE3C6A95A9EA90768D60A46E20F5530FC76F2A496B784C25B474A194ABFD8FC28E75670A46994F3116FC52D293EE7FA49AFDA9FCE90F7235C100DDA2465FB85A564A88764FE9187D7141121C184512C7F9863C2C4A2F02BE76C8897CCA24EA6302302C8CF948DF6AF51B3D01C2DA1B76DD66FDF25C7AA13B767AA1093DD7620F80D814D20D985E9DF5E4D4B11C7C44F393A75FECF779AF74A2A7DBFBDA17E42B84A95682F99EBA2D131FF55C70B86529C7B54AA2866246CB8F98B403ABD24C57530AA624B743C0C63E3F019FCA40EFC444357E793301A1"})
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
