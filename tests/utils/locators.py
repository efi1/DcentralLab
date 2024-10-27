from selenium.webdriver.common.by import By
from tests.utils.locator import Locator


class Staging:

    @property
    def page_displayed(self):
        return Locator(By.CSS_SELECTOR, "[class='create-farm app']")

    @property
    def open(self):
        return Locator(By.ID, "farm-chain")

    @property
    def get_listbox_css(self):
        return Locator(By.CSS_SELECTOR, "[id^='react-select-2-option']")

    @property
    def get_listbox_xpath(self):
        return Locator(By.XPATH, "//*[starts-with(@id, 'react-select-2-option')]")

    @property
    def get_selected_item(self):
        return Locator(By.CLASS_NAME, 'network-label')

    @property
    def is_container_message(self):
        return Locator(By.CSS_SELECTOR, "span[class='web3-wc_modal-icon-btn web3-wc_close-modal-btn']")


class HordLocators:

    @property
    def sidebar(self):
        return Locator(By.CLASS_NAME, "passed-content-wrapper"), Locator(By.CLASS_NAME, "sidebar-toggle-wrapper")

    @property
    def sidebar_verification(self):
        return Locator(By.XPATH, "//*[contains(@class, 'expanded')]")

    @property
    def faq_wrapper(self):
        return Locator(By.CLASS_NAME, "faq-question-wrapper")

    @property
    def faq_links_desc(self):
        return Locator(By.XPATH, "//*[@class='parent-content']/article/span")

    @property
    def goto_revenue_share(self):
        return Locator(By.XPATH, "//span[text()='Revenue Share']")

    @property
    def revenue_list(self):
        return Locator(By.XPATH, "//*[contains(@class, 'revenue-share-history-wrapper')]/div")


class MainPageLocators:
    go_bottom = Locator(By.TAG_NAME, "html")
