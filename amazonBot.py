import os
import time

from logger import logger as l
from selenium.common.exceptions import *

LOGIN_MAIL = os.environ.get('LOGIN_MAIL', None)
LOGIN_PASSWORD = os.environ.get('LOGIN_PASSWORD', None)

ITEM_URL = os.environ.get('ITEM_URL', None)

ACCEPT_SHOP = 'Amazon.com'
LIMIT_VALUE = 50    # Maximum USD for the purchase

def login(chromeDriver, email, password):
    try:
        chromeDriver.find_element_by_id("nav-link-accountList").click()
        l.info('Login in with email: {}'.format(email))
        chromeDriver.find_element_by_id('ap_email').send_keys(email)
        chromeDriver.find_element_by_id('continue').click()
        chromeDriver.find_element_by_id('ap_password').send_keys(password)
        chromeDriver.find_element_by_id('signInSubmit').click()
        l.info('Successfully logged in!')
    except Exception as e:
        l.error('Error loggin in: {}'.format(e))

def purchase_item(chromeDriver, url, limitValue, seller):
    l.info("Purchasing item...")
    chromeDriver.get(url)
    # Checks if out of stock, verify_stock returns False if not in stock
    inStock = in_stock_check(chromeDriver)
    if not inStock:
        return False
    # Checks price
    if not verify_price_within_limit(chromeDriver, limitValue):
        return False
    # Checks seller
    seller_check(chromeDriver, seller)

    chromeDriver.find_element_by_id('buy-now-button').click()  # 1 click buy
    chromeDriver.find_element_by_id('turbo-checkout-pyo-button').click()


def in_stock_check(chromeDriver):
    l.info("Checking stock...")
    inStock = False
    try:
        shop = chromeDriver.find_element_by_id('tabular-buybox-truncate-1').text
        l.info("Text from shop: {}".format(shop))
        try:
            chromeDriver.find_element_by_id("outOfStock")
            l.info("Item is outOfStock")
            chromeDriver.refresh()
        except Exception as e:
            try:
                chromeDriver.find_element_by_id("merchant-info")
                l.info("Item is in-stock!")
                inStock = True
            except Exception as e:
                time.sleep(1)
                l.error('Could not find merchant info, refreshing...')
                chromeDriver.refresh()
    except Exception as e:
        l.error('Error checking stock: {}'.format(e))
    finally:
        return inStock

def seller_check(chromeDriver, seller):
    element = chromeDriver.find_element_by_id("merchant-info")
    shop = element.text.find(seller)
    if shop == -1:
        raise Exception("Amazon is not the seller")
    l.info("Successfully verified Seller")

def verify_price_within_limit(chromeDriver, limitValue):
    price = chromeDriver.find_element_by_id('priceblock_ourprice').text
    l.info('price of item is:  ', price)
    if int(price.replace(' ', '').replace(',', '').replace('$', '')) > limitValue:
        l.warn('PRICE IS TOO LARGE.')
        return False
    return True

