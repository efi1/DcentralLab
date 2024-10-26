from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from tests.pages.base_page import BasePage
from tests.utils.locators import HordLocators


class HordPage(BasePage, HordLocators):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.locators = HordLocators()

    @property
    def get_sidebar_ele(self) -> object:
        locator_a, locator_b = self.locators.sidebar
        ele = self.find_element(locator_a)
        return ele.find_element(locator_b.by, locator_b.value)

    @property
    def toggle_sidebar(self) -> None:
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
        faq_items = self.find_elements(self.locators.faq_wrapper, expected_condition='visibility')
        return faq_items

    @classmethod
    def verify_faq_titles(cls, faq_items: list) -> list:
        items_text = [item.text for item in faq_items]
        return items_text

    def verify_faq_links(self, faq_items: list) -> tuple[bool, list]:
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
                print(F"faq link is not clickable")
                return False, []
            desc.append(item.find_element(self.locators.faq_links_desc.by, self.locators.faq_links_desc.value).text)
        return True, desc
