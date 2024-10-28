import inspect
import logging
import time
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains, Keys
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

    @BasePage.retry_unreachable_element
    @BasePage.logger
    def toggle_sidebar(self) -> None:
        element = self.get_sidebar_ele
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()
        element.click()

    @property
    @BasePage.logger
    def is_sidebar_expand(self) -> bool:
        """
        Searching for expended elements.
        :return: True if found
        """
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
        faq_items = self.find_elements(self.locators.faq_wrapper, expected_condition='visibility')
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
            item_desc = item.find_element(self.locators.faq_links_desc.by, self.locators.faq_links_desc.value).text
            desc.append(item_desc)
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
        self.find_element(self.locators.goto_revenue_share, expected_condition='presence').click()

    def wait_for_revenue_list(self, timeout=10) -> list:
        start_time = time.time()
        while time.time() - start_time < timeout:
            elements = self.find_elements(self.locators.revenue_list)
            if len(elements) > 1:
                break
            time.sleep(1)
        return elements

    @property
    @BasePage.logger
    def get_revenue_content(self) -> list:
        elements = self.wait_for_revenue_list()
        return [item.text for item in elements]
