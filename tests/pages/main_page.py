import logging
import time
import inspect
from tests.pages.base_page import BasePage
from tests.pages.staging_page import StagingPage
from tests.pages.hord_page import HordPage
from tests.utils.locators import MainPageLocators as Locators
from selenium.webdriver.common.keys import Keys

LOGGER = logging.getLogger()


class MainPage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)

    def navigate(self, url=None, is_displayed_locator=None):
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        self.navigate_to(url, is_displayed_locator)

    @BasePage.logger
    def go_to_staging(self, base_url, search_type=None):
        # LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        return StagingPage(self.driver, base_url, search_type)

    @BasePage.logger
    def go_to_hord(self, base_url):
        # LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        return HordPage(self.driver, base_url)

    @property
    def go_bottom(self):
        ele = self.find_element(Locators.get_page, expected_condition='presence')
        ele.send_keys(Keys.END)
        time.sleep(2)


    @property
    def got_up(self):
        ele = self.find_element(Locators.get_page, expected_condition='presence')
        ele.send_keys(Keys.PAGE_UP)
        time.sleep(1)