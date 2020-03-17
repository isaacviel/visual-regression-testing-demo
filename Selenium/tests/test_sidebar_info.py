#!/usr/bin/python3

from unittest import TestCase, main

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Test(TestCase):

    def setUp(self):

        # Browser capabilities
        caps = {
            'browserName': 'chrome'
        }

        self.driver = webdriver.Remote(
            # local grid
            command_executor='http://localhost:4444/wd/hub',

            # hosted grid
            # command_executor='http://dev0011821.esri.com:4444/wd/hub',

            desired_capabilities=caps
        )

        # Assign wait time across the test (sec)
        self.driver.implicitly_wait(5)

        # Create empty list for error messages
        self.verificationErrors = []

    def test_map_attributes(self):

        driver = self.driver
        driver.set_window_size(1366, 900)

        # Navigate browser to home page
        driver.get('http://host.docker.internal:4200')

        # Original series info windows
        tos_info = WebDriverWait(driver, 90).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.series-tos')))

        # Check that there are the correct number of info windows for The Original Series
        try:
            self.assertEqual(len(tos_info), 7)
        except AssertionError as e:
            self.verificationErrors.append(
                'Test 1 failed: Incorrect number of TOS' + str(e))

        # The Next Generation info windows
        tng_info = WebDriverWait(driver, 90).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.series-tng')))

        # Check that there are the correct number of info windows for The Next Generation
        try:
            self.assertEqual(len(tng_info), 3)
        except AssertionError as e:
            self.verificationErrors.append(
                'Test 1 failed: Incorrect number of TNG ' + str(e))

    def tearDown(self):
        # Quit driver
        self.driver.quit()

        # Check that there are no errors stored from the test.
        self.assertEqual([], self.verificationErrors)


if __name__ == '__main__':
    main(warnings='ignore')
