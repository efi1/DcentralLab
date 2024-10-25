import time

from tests.pages.base_page import BasePage
from tests.pages.staging_page import StagingPage
from tests.pages.hord_page import HordPage
from tests.utils.locators import MainPageLocators as Locators
from selenium.webdriver.common.keys import Keys


class MainPage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)

    def navigate(self, is_displayed_locator=None):
        # page = MainPage(driver, url)
        self.navigate_to(is_displayed_locator)

    def go_to_staging(self, url, search_type=None):
        return StagingPage(self.driver, url, search_type)

    def go_to_hord(self, url):
        return HordPage(self.driver, url)

    @property
    def go_bottom(self):
        ele = self.find_element(Locators.go_bottom, expected_condition='presence')
        ele.send_keys(Keys.END)
        time.sleep(1)
