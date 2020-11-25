import os
import time

from logger import logger as l
from selenium.common.exceptions import *

LOGIN_MAIL = os.environ.get('LOGIN_MAIL', None)
LOGIN_PASSWORD = os.environ.get('LOGIN_PASSWORD', None)

ITEM_URL = os.environ.get('ITEM_URL', None)

ACCEPT_SHOP = 'Amazon.com'
LIMIT_VALUE = 50    # Maximum USD for the purchase



def login(chromeDriver):
    chromeDriver.find_element_by_id("nav-link-accountList").click()
    chromeDriver.find_element_by_id('ap_email').send_keys(LOGIN_MAIL)
    chromeDriver.find_element_by_id('continue').click()
    chromeDriver.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
    chromeDriver.find_element_by_id('signInSubmit').click()

def purchase_item(chromeDriver):
    chromeDriver.get(ITEM_URL)
    # Checks if out of stock, verify_stock returns False if not in stock
    if not in_stock_check(chromeDriver):
        return False
    # Checks price
    if not verify_price_within_limit(chromeDriver):
        return False
    # Checks seller
    verify_price_within_limit(chromeDriver)

    chromeDriver.find_element_by_id('buy-now-button').click()  # 1 click buy
    chromeDriver.find_element_by_id('turbo-checkout-pyo-button').click()


def in_stock_check(chromeDriver):
    inStock = False
    try:
        shop = chromeDriver.find_element_by_id('tabular-buybox-truncate-1').text
        try:
            chromeDriver.find_element_by_id("outOfStock")
            l.info("Item is outOfStock")
            chromeDriver.refresh()
        except NoSuchElementException as e:
            try:
                chromeDriver.find_element_by_id("merchant-info")
                l.info("Item is in-stock!")
                inStock = True
            except NoSuchElementException as e:
                time.sleep(1)
                chromeDriver.refresh()
    finally:
        return inStock

def seller_check(chromeDriver):
    element = chromeDriver.find_element_by_id("merchant-info")
    shop = element.text.find(ACCEPT_SHOP)
    if shop == -1:
        raise Exception("Amazon is not the seller")
    l.info("Successfully verified Seller")

def verify_price_within_limit(chromeDriver):
    price = chromeDriver.find_element_by_id('priceblock_ourprice').text
    l.info('price of item is:  ', price)
    if int(price.replace(' ', '').replace(',', '').replace('$', '')) > LIMIT_VALUE:
        l.warn('PRICE IS TOO LARGE.')
        return False
    return True

