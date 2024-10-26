import inspect
import logging
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import WebDriverException, TimeoutException
from tests.pages.base_page import BasePage
from tests.utils.locators import ListboxLocators


LOGGER = logging.getLogger()


class StagingPage(BasePage, ListboxLocators):
    def __init__(self, driver, base_url, search_type=None):
        super().__init__(driver, base_url)
        self.locators = ListboxLocators()
        self.find_locator = self.locators.get_list_css if search_type == 'css' else self.locators.get_list_xpath

    @staticmethod
    def suppress_container_message(func):
        """ supress popup overlay container"""
        def wrapper(self, *args, **kwargs):
            try:
                is_container = self.find_element(self.locators.is_container_message, timeout_sec=2,
                                                 expected_condition='clickable')
                is_container.click()
            except (EC.StaleElementReferenceException, TimeoutException) as e:
                return func(self, *args, **kwargs)

        return wrapper

    def open_listbox(self) -> None:
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        try:
            self.find_element(self.locators.open).click()
        except WebDriverException as e:
            print(e)
            # LOGGER(e)

    @suppress_container_message
    def get_listbox(self) -> list:
        """ get all listbox elements"""
        try:
            listbox = self.find_elements(self.find_locator, timeout_sec=2)
        except TimeoutException:
            self.open_listbox()
            listbox = self.find_elements(self.find_locator, timeout_sec=2)
        return listbox

    @suppress_container_message
    def get_valid_listbox(self, listbox, timeout=5) -> list:
        """ verify that listbox elements are valid, if not retrieve them again """
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        start_time = time.time()
        while time.time() - start_time <= timeout:
            if not listbox or listbox[0].aria_role == 'none':
                listbox = self.get_listbox
                time.sleep(1)
            else:
                return listbox

    def select_item_listbox(self, listbox: list, chain_name: str) -> None:
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        self.get_valid_listbox(listbox)
        for item in listbox:
            if item.text == chain_name:
                item.click()
                break

    @property
    def get_selected_item(self) -> str:
        """ get the selected item name """
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        return self.find_element(self.locators.get_selected_item).text
