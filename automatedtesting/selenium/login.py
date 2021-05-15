# #!/usr/bin/env python3
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

Locators = {'id_username': 'user-name', 'id_password': 'password', 'id_login': 'login-button',
            'class_add_to_cart': 'inventory_item', 'class_remove': 'btn_secondary '}


def timestamp():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return ts + '\t'


# Start the browser and login with standard_user
def login(user_name, password):
    print(timestamp() + 'Starting the browser...')
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    # chrome_driver = webdriver.Chrome('/Users/marco/Downloads/chromedriver')
    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.get('https://www.saucedemo.com/')

    print(timestamp() + 'Browser started successfully. Navigating to the demo page to login.')
    chrome_driver.find_element_by_id(Locators['id_username']).send_keys(user_name)
    chrome_driver.find_element_by_id(Locators['id_password']).send_keys(password)
    chrome_driver.find_element_by_id("login-button").click()
    print(timestamp() + 'Login with username {:s} and password {:s} successfully.'.format(user_name, password))
    return chrome_driver


def add_cart(driver):
    print(timestamp() + 'Add all element to cart')
    list_add_to_cart = driver.find_elements_by_class_name(
        Locators['class_add_to_cart'])

    for element in list_add_to_cart:
        item_name = element.find_element_by_class_name(
            'inventory_item_name').text
        element.find_element_by_class_name('btn_inventory').click()
        print(timestamp() + 'Added {} to cart'.format(item_name))

    driver.find_element_by_class_name('shopping_cart_link').click()
    print(timestamp() + f'{len(list_add_to_cart)} items were added to shopping the cart successfully.')


def remove_cart(driver):
    for item in driver.find_elements_by_class_name('cart_item'):
        item_name = item.find_element_by_class_name('inventory_item_name').text
        item.find_element_by_class_name('cart_button').click()
        print(timestamp() + 'Removed {} from cart'.format(item_name))

    driver.find_element_by_class_name('btn_secondary').click()
    print(timestamp() + 'All items were removed from the shopping cart successfully.')


if __name__ == "__main__":
    chrome_driver = login(user_name='standard_user', password='secret_sauce')
    add_cart(driver=chrome_driver)
    remove_cart(driver=chrome_driver)
    print(timestamp() + 'Selenium tests are all successfully completed!')
