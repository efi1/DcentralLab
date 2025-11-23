import inspect
import logging
import time
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from tests.pages.base_page import BasePage
from tests.utils.locators import HordLocators

LOGGER = logging.getLogger()


class HordPage(BasePage, HordLocators):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.locators = HordLocators()


    @property
    @BasePage.logger
    def get_sidebar_ele(self) -> WebElement:
        # LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        locator_a, locator_b = self.locators.sidebar
        ele = self.search_element(locator_a, expected_condition='visibility')
        # s1 = ele.find_element(locator_b.by, locator_b.value)
        return self.search_element(locator_b, element=ele, expected_condition='clickable', timeout_sec=15)


    @property
    @BasePage.logger
    @BasePage.retry_unreachable_element
    def get_action_chains(self) -> WebElement:
        element = self.get_sidebar_ele
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
        except Exception as e:
            LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}, move mouse failed: {e}")
        return element

    @BasePage.logger
    def toggle_sidebar(self, element) -> None:
        element.click()

    @property
    @BasePage.logger
    def is_sidebar_expand(self) -> bool:
        """
        Searching for expended elements.
        :return: True if found
        """
        try:
            self.search_elements(self.locators.sidebar_verification, timeout_sec=10)
            return True
        except TimeoutException:
            return False

    @property
    def get_faq_items(self) -> list:
        """
        :return: a list of all faq elements
        """
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        faq_items = self.search_elements(self.locators.faq_wrapper, expected_condition='presence')
        LOGGER.info(F"++++ exit {inspect.currentframe().f_code.co_name}, result: {faq_items}")
        return faq_items

    @classmethod
    @BasePage.logger
    def verify_faq_titles(cls, faq_items: list) -> list:
        items_text = [item.text for item in faq_items]
        return items_text

    @BasePage.logger
    def verify_faq_answer_links(self, faq_items: list) -> list:
        """
        Verify that all links are clickable and return their description.
        :param faq_items: faq elements
        :return: True if clickable and the links' entire content.
        """
        desc = []
        for item in faq_items:
            try:
                item.click()
            except WebDriverException:
                LOGGER.info(F"faq link is not clickable")
                return []
            # item_desc = item.find_element(self.locators.faq_links_desc.by, self.locators.faq_links_desc.value).text
            time.sleep(2)
            item_desc = self.search_element(self.locators.faq_links_desc, item).text
            desc.append(item_desc)
            # item.click()
        return desc

    @property
    @BasePage.logger
    def verify_links_functionality(self):
        items = self.get_faq_items
        for item in items:
            if any([not self.is_clickable(item), not self.is_clickable(item)]):
                return False
        return True

    #
    @BasePage.retry_unreachable_element
    def click_on_revenue_share(self):
        self.search_element(self.locators.goto_revenue_share, expected_condition='clickable').click()

    def wait_for_revenue_list(self, timeout=10) -> list:
        start_time = time.time()
        while time.time() - start_time < timeout:
            elements = self.search_elements(self.locators.revenue_list)
            if len(elements) > 1:
                break
            time.sleep(1)
        return elements

    @property
    @BasePage.logger
    def get_revenue_content(self) -> list:
        elements = self.wait_for_revenue_list()
        return [item.text for item in elements]
