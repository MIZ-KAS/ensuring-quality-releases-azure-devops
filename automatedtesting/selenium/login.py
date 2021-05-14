# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import logging
import sys


# Start the browser and login with standard_user


def login(user, password):
    print('Starting the browser...')
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    # driver = webdriver.Chrome()
    print('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')

    logging.info('Loging in to https://www.saucedemo.com/')
    driver.find_element_by_css_selector(
        'input[data-test="username"]').send_keys(user)
    driver.find_element_by_css_selector(
        'input[data-test="password"]').send_keys(password)
    driver.find_element_by_css_selector('input[value=LOGIN]').click()

    logging.info('Searching for Products')
    headerLabel = driver.find_element_by_class_name('product_label').text
    assert "Products" in headerLabel
    logging.info('Successfully logged in, user: ' + user)

    logging.info('Find products')
    products = driver.find_elements_by_css_selector('.inventory_item')

    logging.info('Add products to cart')
    for product in products:
        product_name = product.find_element_by_css_selector(
            '.inventory_item_name').text
        product.find_element_by_css_selector('button.btn_inventory').click()
        logging.info('Product added to cart: ' + product_name)

    logging.info('Verify if cart has 6 added products')
    cart_label = driver.find_element_by_css_selector(
        '.shopping_cart_badge').text
    assert cart_label == '6'

    logging.info('Navigate to cart')
    driver.find_element_by_css_selector('a.shopping_cart_link').click()
    assert '/cart.html' in driver.current_url, 'Cart navigation unsuccessful'

    logging.info('Removing products from cart')
    cart_products = driver.find_elements_by_css_selector('.cart_item')
    for product in cart_products:
        product_name = product.find_element_by_css_selector(
            '.inventory_item_name').text
        product.find_element_by_css_selector('button.cart_button').click()
        logging.info('Removed from cart: ' + product_name)

    logging.info('Verify if cart is empty')
    if driver.find_elements_by_css_selector('.shopping_cart_badge'):
        logging.info('Cart is empty')
        cart_state = 1
    else:
        cart_state = 0

    logging.info('Cart state: ' + str(cart_state))
    assert cart_state == 0


login('standard_user', 'secret_sauce')
