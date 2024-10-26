import inspect
import logging
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EXPECTED_CONDITIONS_ELEMENT = \
    {
        'visibility': 'visibility_of_element_located',
        'presence': 'presence_of_element_located',
        'clickable': 'element_to_be_clickable'
    }

EXPECTED_CONDITIONS_ELEMENTS = \
    {
        'visibility': 'visibility_of_all_elements_located',
        'presence': 'presence_of_all_elements_located',
    }


LOGGER = logging.getLogger()


class BasePage(object):
    def __init__(self, driver, base_url):
        self.base_url = [base_url] if isinstance(base_url, str) else base_url
        self.driver = driver

    def find_element(self, locator, expected_condition='presence', timeout_sec=10, ignored_exceptions=None):
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}, locators: {locator.by, locator.value}, "
                    F"expected condition: {expected_condition}")
        return (WebDriverWait(self.driver, timeout_sec, ignored_exceptions=ignored_exceptions).until(
            getattr(EC, EXPECTED_CONDITIONS_ELEMENT.get(expected_condition))(locator),
            message=f"Can't find element by locator {locator}"))

    def find_elements(self, locator, expected_condition='presence', timeout_sec=10, ignored_exceptions=None):
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}, locators: {locator.by, locator.value}, "
                    F"expected condition: {expected_condition}")
        return WebDriverWait(self.driver, timeout_sec, ignored_exceptions=ignored_exceptions).until(
            getattr(EC, EXPECTED_CONDITIONS_ELEMENTS.get(expected_condition))(locator),
            message=f"Can't find elements by locator {locator}")

    def click_on(self, locator, timeout_sec=10):
        self.find_element(locator, expected_condition='clickable', timeout_sec=timeout_sec).click()

    def navigate_to(self, url=None, page_displayed=None):
        for uri in self.base_url:
            uri = F"{uri}/{url}" if url else uri
            try:
                self.driver.get(uri)
                if page_displayed:
                    self.find_element(page_displayed, expected_condition='visibility', timeout_sec=2)
                break
            except TimeoutException as e:
                LOGGER.info(F"**** Page Display Error when navigate to: {uri}")

