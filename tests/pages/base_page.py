import time
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
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


class BasePage(object):
    def __init__(self, driver, base_url):
        self.base_url = [base_url] if isinstance(base_url, str) else base_url
        self.driver = driver

    def find_element(self, locator, expected_condition='presence', timeout_sec=10, ignored_exceptions=None):
        return (WebDriverWait(self.driver, timeout_sec, ignored_exceptions=ignored_exceptions).until(
            getattr(EC, EXPECTED_CONDITIONS_ELEMENT.get(expected_condition))(locator),
            message=f"Can't find element by locator {locator}"))

    def find_elements(self, locator, expected_condition='presence', timeout_sec=10, ignored_exceptions=None):
        return WebDriverWait(self.driver, timeout_sec, ignored_exceptions=ignored_exceptions).until(
            getattr(EC, EXPECTED_CONDITIONS_ELEMENTS.get(expected_condition))(locator),
            message=f"Can't find elements by locator {locator}")

    def click_on(self, locator, timeout_sec=10):
        self.find_element(locator, expected_condition='clickable', timeout_sec=timeout_sec).click()

    def navigate_to(self, url='', is_displayed_locator=None):
        for uri in self.base_url:
            uri += url
            try:
                self.driver.get(uri)
                if is_displayed_locator:
                    self.find_element(is_displayed_locator, expected_condition='visibility', timeout_sec=2)
                break
            except TimeoutException as e:
                print(F"Error when navigate to: {uri}, {e}")
        # time.sleep(3)

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def enter_txt(self, locator, txt):
        self.find_element(locator).send_keys(txt)

    def wait_until_visibility_of_element_located(self, locator):
        WebDriverWait(self.driver, timeout=5).until(EC.visibility_of_element_located(locator))

