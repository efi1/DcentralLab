import inspect
import logging
import time
from functools import wraps
from _ctypes_test import func
from selenium.common import TimeoutException, WebDriverException, ElementClickInterceptedException
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

    def find_element(self, locator, element=None, expected_condition='presence', timeout_sec=10,
                     ignored_exceptions=None):
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}, locators: {locator.by, locator.value}, "
                    F"expected condition: {expected_condition}")
        return (
            WebDriverWait(element if element else self.driver, timeout_sec,
                          ignored_exceptions=ignored_exceptions).until(
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
        time.sleep(3)

    @classmethod
    def is_clickable(cls, item: object):
        try:
            item.click()
        except WebDriverException:
            LOGGER.info(F"item is not clickable")
            return False
        return True

    @staticmethod
    def retry_unreachable_element(func) -> object:
        """
        it retries func exec when StaleElementReferenceException or ElementClickInterceptedException occur.
        :param func: the wrapped function.
        :return: the function execution result.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            counter = 0
            retries = kwargs.get('retries', 5)
            while counter <= retries:
                try:
                    return func(*args, **kwargs)
                except (EC.StaleElementReferenceException, ElementClickInterceptedException) as e:
                    LOGGER.info(F"Error occurred:\n{e.msg}\nRetrying...")
                    counter += 1

            raise Exception("***   element is not clickable")

        return wrapper

    @classmethod
    def logger(cls, func):
        """
        A decorator function to log information about function calls and their results.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            The wrapper function that logs function calls and their results.
            """
            LOGGER.info(f"\n++++ Running {func.__name__} with args: {args}, kwargs: {kwargs}")
            try:
                result = func(*args, **kwargs)
                LOGGER.info(f"++++ Finished {func.__name__} with result: {result}\n")

            except Exception as e:
                LOGGER.error(f"++++ Error occurred in {func.__name__}: {e}\n")
                raise

            else:
                return result
        return wrapper
