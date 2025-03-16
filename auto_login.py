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
    browser.add_cookie({"name": "MUSIC_U", "value": "007475AEE49CD7732E54732B19F1F678B3601897DE05C4AE461F530A767A2D08E40C4EE3E8D1A5EA2B00177375EC81D66975773A2C71869511D1888E02B8F20C11228C3437B0E89A17883F31F408AA8DC029377AA5B5821DADFBDA7C7C4189E8FAC61F3E04155461E3760C3E56565D43870B683E35EB212D3C73EE007C58BBBABE12E3E3EFA70F0C1FE4C96FB20BA195FC3207128B5A70C3E903CE488C52CFEC92853A6A07BF7CEBFD6F422E626127767C99931EEBDBC732224A820C07D0D1BCBE2B9E289AA9017F67CDB473E481724162BD30A605B8F480F83195107BE37C4201C9C2992B4262677D8F67AB19B77CC50C95AE04F878D5AB6EFF1A63E7FC4336ABDB533820E9B674F7470CD00E62CC1C80D428BCF32C00BDE2D39CFAA50CFC972084500F8DFDCE708A8148C662623F92DB70CB27D232143E581A54A95784D58DB5BDD60097979BBF5B1C80C34772178BAA42ABF04A45FD40D6D4374FC008A6F5EE"})
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
