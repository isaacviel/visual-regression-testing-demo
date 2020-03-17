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

        map_center = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'app-esri-map')))
        map_center_val = map_center.get_attribute("ng-reflect-center")

        # Check that map is centered where expected
        try:
            self.assertEqual(map_center_val, '-118.3862,34.1423')
        except AssertionError as e:
            self.verificationErrors.append(
                'Test 1 failed: Map center not expected ' + str(e))

        map_zoom = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'app-esri-map')))
        map_zoom_val = map_zoom.get_attribute("ng-reflect-zoom")

        # Check that map zoom level is as expected
        try:
            self.assertEqual(map_zoom_val, '9')
        except AssertionError as e:
            self.verificationErrors.append(
                'Test 2 failed: Map zoom not correct ' + str(e))

        map_attribution = WebDriverWait(driver, 90).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.esri-attribution__sources.esri-interactive')))

        # Check that map attribution is correct
        try:
            self.assertEqual(
                map_attribution.text, 'County of Los Angeles, Esri, HERE, Garmin, SafeGraph, FAO, METI/NASA, USGS, Bureau of Land Management, EPA, NPS')
        except AssertionError as e:
            self.verificationErrors.append(
                'Test 3 failed: Map attribution is not corrrect ' + str(e))

    def tearDown(self):
        # Quit driver
        self.driver.quit()

        # Check that there are no errors stored from the test.
        self.assertEqual([], self.verificationErrors)


if __name__ == '__main__':
    main(warnings='ignore')
