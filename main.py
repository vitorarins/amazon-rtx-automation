#coding: utf-8

import time
import os
import amazonBot
from os.path import join, dirname
from datetime import datetime
from selenium import webdriver
from logger import logger
from dotenv import load_dotenv
from selenium.webdriver import DesiredCapabilities

DELAY = 32

load_dotenv(verbose=True)
dotenv_path = '.env'
load_dotenv(dotenv_path)

def launch():
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    opt.add_argument("--disable-xss-auditor")
    opt.add_argument("--disable-web-security")
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument("--allow-running-insecure-content")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--headless")
    opt.add_argument("--remote-debugging-port=921")
    opt.add_argument("--disable-webgl")
    opt.add_argument("--disable-popup-blocking")
    opt.add_argument("--user-data-dir=selenium") # added this option to use cookies, you may need to perform initial login within Selenium
    browser = webdriver.Chrome('chromedriver' ,options=opt,desired_capabilities=d)
    browser.implicitly_wait(10)
    browser.set_page_load_timeout(5)
    logger.info('Started Chrome')
    return browser

if __name__ == '__main__':
    url = os.environ.get('ITEM_URL', None)
    # Launch selenium
    try:
        b = launch()
        logger.info('Now opening: {}'.format(url))
        b.get(url)
    except Exception as inst:
        logger.error('Failed to open browser: {}'.format(format(inst)))
        exit()

    # Log in
    try:
        amazonBot.login(b)
    except Exception as e:
        logger.error('Error Could not login: {}'.format(e))
        exit()

    # Item purchasing logic
    try:
        done = False
        while(not done):
            try:
                # Navigate to the item and buy if checks pass
                amazonBot.purchase_item(b)
                done = True
                logger.info("Successfully purchased item")
            except BaseException:
                pass
            except Exception as e:
                logger.error('ERROR: {}'.format(e))
            time.sleep(DELAY)
    finally:
        logger.info('Closing Chromium')
        try:
            b.close()
        except BaseException:
            pass
        logger.info('Closed Chromium')
