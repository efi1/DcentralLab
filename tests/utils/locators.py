from selenium.webdriver.common.by import By
from collections import namedtuple

Locator = namedtuple('locator', ['by', 'value'])


class ListboxLocators:
    @property
    def open_listbox(self):
        s = Locator(By.ID, "farm-chain")
        return Locator(By.ID, "farm-chain")

    @property
    def get_listbox_css(self):
        return Locator(By.CSS_SELECTOR, "[id^='react-select-2-option']")

    @property
    def get_listbox_xpath(self):
        return Locator(By.XPATH, "//div[@id='react-select-2-listbox']")

    @property
    def get_selected_item(self):
        return Locator(By.CLASS_NAME, 'network-label')


class MainPageLocators:
    pass
