#!/usr/bin/python3

from os import getenv
from time import sleep
from urllib.parse import urlsplit

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def set_driver(self, waitTime):
    """Sets the driver for the test and assigns capabilities"""

    caps = {
        'browserName': getenv('BROWSER', 'chrome')
   }

    self.driver = webdriver.Remote(
        # local grid
        command_executor='http://localhost:4444/wd/hub',
        
        # hosted grid
        # command_executor='http://dev0011821.esri.com:4444/wd/hub',
        
        desired_capabilities=caps
    )

    # Assign wait time across the test (sec)
    self.driver.implicitly_wait(waitTime)

    # Create empty list for error messages
    self.verificationErrors = []


def end_tasks(self):
    '''Quits test, closes browser and sends errors to console.'''

    # Quit driver
    self.driver.quit()

    # Check that there are no errors stored from the test.
    self.assertEqual([], self.verificationErrors)

# ~~~~~ Site-specific page object methods ~~~~~


def log_into_site(driver, environment, user, password):
    """logs the browser into the site"""

    # Get the homepage to insert the following cookie
    driver.get(environment + '/')

    # Add GDPR Cookie to remove banner
    driver.add_cookie({'name': 'esri_gdpr', 'value': 'true',
                       'path': '/', 'domain': '.arcgis.com'})

    # Navigate browser to sign-in page
    driver.get(environment + '/sign-in/')

    # Switch to iframe content
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))

    # Login via oAuth
    # Enter username
    userield = driver.find_element(By.NAME, 'username')
    userield.clear()
    userield.send_keys(user)

    # Enter password
    user_password = driver.find_element(By.NAME, 'password')
    user_password.clear()
    user_password.send_keys(password)

    # Click sign in button
    sign_in_button = driver.find_element(By.ID, 'signIn')
    sign_in_button.click()

    # Switch back to main content
    driver.switch_to.default_content()

    # wait for cookie to set a few seconds. sadly needed :/
    sleep(5)


def log_out_of_site(self, driver):
    """Logs the webdriver out of site"""

    # Click profile dropdown
    profile_dropdown = driver.find_element(By.CSS_SELECTOR, '.user-nav-name')
    profile_dropdown.click()

    # Click log out button in profile dropdown
    log_out_button = driver.find_element(By.CSS_SELECTOR,
                                         'developers-sign-out')
    log_out_button.click()


def delete_application(driver):
    """Deletes test application create by this test"""

    # Click on Settings tab
    settings_tab = driver.find_element(By.LINK_TEXT, 'Settings')
    settings_tab.click()

    # Check is the delete prevention check box is checked
    delete_blocker = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name=\"deletePrevention\"]')))

    # If delete prevention check box is checked, uncheck it
    if delete_blocker.is_selected():
        delete_blocker.click()

    # Waits for delete button to be visible then clicks
    del_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'button[calcitemodaltoggle=\"delete-modal\"].btn')))
    del_button.click()

    # Waits for delete button to be visible then clicks
    delete_confirm_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn.btn-red')))
    delete_confirm_button.click()

    # Waits for delete button to be visible then clicks
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[_ngcontent-c12].modal-content.column-12')))


def shield_log_in(self, environment, driver, authUser, authPass):
    """Log into the QA / Dev Ext site"""

    driver.get(environment)

    if environment == 'https://developersdevext.arcgis.com' or environment == 'https://developersqa.arcgis.com':
        dev_user = driver.find_element(By.CSS_SELECTOR, '#j_username')
        dev_user.clear()
        dev_user.send_keys(authUser)
        dev_pass = driver.find_element(By.CSS_SELECTOR, '#j_password')
        dev_pass.clear()
        dev_pass.send_keys(authPass)
        auth_button = driver.find_element(By.CSS_SELECTOR, '#submit')
        auth_button.click()
    else:
        pass


def extract_item_id(current_url):
    """Takes the current URL from the tests then extracts and returns
    the Item ID"""

    # Breaks the URL into pieces using urlsplit
    break_up_url = urlsplit(current_url)

    # Extracts the the path and splits it at the /
    the_path = break_up_url.path.split('/')

    # Returns the third path item, which should be the Item ID
    return the_path[2]
