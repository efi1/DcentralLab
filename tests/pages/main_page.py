from tests.pages.base_page import BasePage
from tests.utils.locators import *
from selenium.webdriver.common.keys import Keys


class MainPage(BasePage):

    @staticmethod
    def navigate(driver, url):
        page = MainPage(driver, url)
        page.navigate_to()
        return page

    def select_from_chains_dropdown(self, chain_name: str) -> str:
        """
        select a chain for a farm's token
        :param chain_name: required chain
        :return: selected chain
        """
        ele = self.find_element((By.TAG_NAME, "html"), expected_condition='presence')
        ele.send_keys(Keys.END)
        locators = ListboxLocators()
        self.open_listbox(locators.open_listbox)
        listbox = self.get_listbox(locators.open_listbox, locators.get_listbox_css)
        self.select_item_listbox(listbox, chain_name)
        selected_item = self.find_element(locators.get_selected_item).text
        return selected_item

