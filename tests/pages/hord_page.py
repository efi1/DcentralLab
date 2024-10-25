from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage
from tests.utils.locators import HordLocators


class HordPage(BasePage, HordLocators):
    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.locators = HordLocators()

    @property
    def get_slidebar_ele(self):
        return self.find_element(self.locators.sidebar)

    @property
    def toggle_sidebar(self):
        element = self.find_element(self.locators.sidebar)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()
        element.click()

    @property
    def is_sidebar_expand(self) -> bool:
        try:
            self.find_elements(self.locators.sidebar_verification, timeout_sec=2)
            return True
        except TimeoutException:
            return False

    @property
    def get_faq_items(self):
        faq_items = self.find_elements(self.locators.faq_wrapper, expected_condition='visibility')
        return faq_items

    @classmethod
    def verify_faq_titles(cls, faq_items):
        items_text = [item.text for item in faq_items]
        return items_text

    @classmethod
    def verify_faq_links(cls, faq_items):
        desc = []
        for item in faq_items:
            try:
                item.click()
            except WebDriverException:
                print(F"faq link is not clickable")
                return False, []
            desc.append(item.find_element(By.XPATH, "//*[@class='parent-content']/article/span").text)
        return True, desc



