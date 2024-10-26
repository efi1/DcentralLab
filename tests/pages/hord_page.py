import inspect
import logging
import time
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from tests.pages.base_page import BasePage
from tests.utils.locators import HordLocators


LOGGER = logging.getLogger()


class HordPage(BasePage, HordLocators):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.locators = HordLocators()

    @property
    def get_sidebar_ele(self) -> object:
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        locator_a, locator_b = self.locators.sidebar
        ele = self.find_element(locator_a)
        return ele.find_element(locator_b.by, locator_b.value)

    @property
    def toggle_sidebar(self) -> None:
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        element = self.get_sidebar_ele
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()
        element.click()

    @property
    def is_sidebar_expand(self) -> bool:
        """
        Searching for expended elements.
        :return: True if found
        """
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        try:
            self.find_elements(self.locators.sidebar_verification, timeout_sec=2)
            return True
        except TimeoutException:
            return False

    @property
    def get_faq_items(self) -> list:
        """
        :return: a list of all faq elements
        """
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        faq_items = self.find_elements(self.locators.faq_wrapper)
        return faq_items

    @classmethod
    def verify_faq_titles(cls, faq_items: list) -> list:
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        items_text = [item.text for item in faq_items]
        return items_text

    def verify_faq_answer_links(self, faq_items: list) -> list:
        """
        Verify that all links are clickable and return their description.
        :param faq_items: faq elements
        :return: True if clickable and the links' entire content.
        """
        LOGGER.info(F"++++ in {inspect.currentframe().f_code.co_name}....")
        desc = []
        for item in faq_items:
            try:
                item.click()
            except WebDriverException:
                LOGGER.info(F"faq link is not clickable")
                return []
            item_desc = item.find_element(self.locators.faq_links_desc.by, self.locators.faq_links_desc.value).text
            desc.append(item_desc)
        return desc

    @property
    def verify_links_functionality(self):
        items = self.get_faq_items
        for item in items:
            if any([not self.is_clickable(item), not self.is_clickable(item)]):
                return False
        return True

    @property
    def click_on_revenue_share(self):
        self.find_element(self.locators.goto_revenue_share, expected_condition='presence').click()

    @property
    def get_revenue_content(self) -> list:
        time.sleep(2) # wait until all elements are loaded
        elements = self.find_elements(self.locators.revenue_list, expected_condition='presence')
        LOGGER.info(F"*** elements number: {len(elements)}, content:\n {elements}")
        return [item.text for item in elements]
