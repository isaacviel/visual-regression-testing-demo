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

    def test_map_attributes(self):
    
        driver = self.driver
        driver.set_window_size(1366, 900)

        # Navigate browser to layers page
        driver.get('http://host.docker.internal:4200')


        map_center = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'app-esri-map')))
        map_center_val = map_center.get_attribute("ng-reflect-center")

        # Check that checkbox is not checked after save
        try:
            self.assertEqual(map_center_val, '-122.4194,37.7749')
        except AssertionError as e:
            self.verificationErrors.append('Test 1 failed: ' + str(e))

        map_zoom = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'app-esri-map')))
        map_zoom_val = map_zoom.get_attribute("ng-reflect-zoom")

        # Check that checkbox is not checked after save
        try:
            self.assertEqual(map_zoom_val, '12')
        except AssertionError as e:
            self.verificationErrors.append('Test 2 failed: ' + str(e))

        map_attribution = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.esri-attribution__sources.esri-interactive')))

        # Check that checkbox is not checked after save
        try:
            self.assertEqual(map_attribution.text, 'USDA FSA, Earthstar Geographics')
        except AssertionError as e:
            self.verificationErrors.append('Test 3 failed: ' + str(e))

    def tearDown(self):
        # Quit driver
        self.driver.quit()

        # Check that there are no errors stored from the test.
        self.assertEqual([], self.verificationErrors)


if __name__ == '__main__':
    main(warnings='ignore')
