import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import WebDriverException, TimeoutException
from tests.pages.base_page import BasePage
from tests.utils.locators import ListboxLocators


class StagingPage(BasePage, ListboxLocators):
    def __init__(self, driver, url, search_type):
        super().__init__(driver, url)
        self.locators = ListboxLocators()
        self.find_locator = self.locators.get_list_css if search_type == 'css' else self.locators.get_list_xpath

    @staticmethod
    def suppress_container_message(func):
        def wrapper(self, *args, **kwargs):
            try:
                is_container = self.find_element(self.locators.is_container_message, timeout_sec=2,
                                                 expected_condition='clickable')
                is_container.click()
            except (EC.StaleElementReferenceException, TimeoutException) as e:
                return func(self, *args, **kwargs)

        return wrapper

    def open_listbox(self) -> None:
        try:
            self.find_element(self.locators.open).click()
        except WebDriverException as e:
            print(e)
            # LOGGER(e)

    @suppress_container_message
    # @property
    def get_listbox(self) -> list:
        try:
            listbox = self.find_elements(self.find_locator, timeout_sec=2)
        except TimeoutException as e:
            self.open_listbox()
            listbox = self.find_elements(self.find_locator, timeout_sec=2)
        return listbox

    def get_valid_listbox(self, listbox, timeout=5) -> list:
        start_time = time.time()
        while time.time() - start_time <= timeout:
            if listbox[0].aria_role == 'none':
                listbox = self.get_listbox
                time.sleep(1)
            else:
                return listbox

    def select_item_listbox(self, listbox: list, chain_name: str) -> None:
        self.get_valid_listbox(listbox)
        for item in listbox:
            if item.text == chain_name:
                item.click()
                break

    @property
    def get_selected_item(self) -> str:
        return self.find_element(self.locators.get_selected_item).text
