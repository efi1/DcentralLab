from selenium.webdriver.common.by import By
from tests.utils.locator import Locator


class ListboxLocators:

    @property
    def is_displayed(self):
        return Locator(By.CSS_SELECTOR, "[class='create-farm app']")

    @property
    def open(self):
        return Locator(By.ID, "farm-chain")

    @property
    def get_list_css(self):
        return Locator(By.CSS_SELECTOR, "[id^='react-select-2-option']")

    @property
    def get_list_xpath(self):
        return Locator(By.XPATH, "//*[contains(@id, 'react-select-2-option')]")

    @property
    def get_selected_item(self):
        return Locator(By.CLASS_NAME, 'network-label')

    @property
    def is_container_message(self):
        return Locator(By.XPATH, "//span[@class='web3-wc_modal-icon-btn web3-wc_close-modal-btn']")


class HordLocators:

    @property
    def sidebar(self):
        return Locator(By.XPATH, "//div[@class='passed-content-wrapper']/div[@class='sidebar-toggle-wrapper']")

    @property
    def sidebar_verification(self):
        return Locator(By.XPATH, "//*[contains(@class, 'expanded')]")

    @property
    def faq_wrapper(self):
        return Locator(By.CLASS_NAME, "faq-question-wrapper")


class MainPageLocators:
    go_bottom = Locator(By.TAG_NAME, "html")
