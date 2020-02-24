#!/usr/bin/python3

import os
from logging import basicConfig, log
from random import choice
from string import ascii_letters, digits
from sys import version
from unittest import TestCase, main
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Test(TestCase):

    def setUp(self):
    
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

    def test_page_title(self):
    
        driver = self.driver
        driver.set_window_size(1366, 900)

        # Navigate browser to layers page
        driver.get('http://host.docker.internal:4200')

        page_title = driver.title

        print(page_title)




        # # Check that checkbox is not checked after save
        # try:
        #     self.assertFalse(editing_check_box.is_selected())
        # except AssertionError as e:
        #     self.verificationErrors.append('Test 2 failed: ' + str(e))

    def tearDown(self):
        # Quit driver
        self.driver.quit()

        # Check that there are no errors stored from the test.
        self.assertEqual([], self.verificationErrors)


if __name__ == '__main__':
    main(warnings='ignore')
