import time
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EXPECTED_CONDITIONS_ELEMENT = \
    {
        'visibility': 'visibility_of_element_located',
        'presence': 'presence_of_element_located',
        'clickable': 'element_to_be_clickable'
    }

EXPECTED_CONDITIONS_ELEMENTS = \
    {
        'visibility': 'visibility_of_all_elements_located',
        'presence': 'presence_of_all_elements_located',
    }


class BasePage(object):
    def __init__(self, driver, base_url):
        self.base_url = base_url
        self.driver = driver

    def find_element(self, locator, expected_condition='presence', timeout_sec=10, ignored_exceptions=None):
        return (WebDriverWait(self.driver, timeout_sec, ignored_exceptions=ignored_exceptions).until(
            getattr(EC, EXPECTED_CONDITIONS_ELEMENT.get(expected_condition))(locator),
            message=f"Can't find element by locator {locator}"))

    def find_elements(self, locator, expected_condition='presence', timeout_sec=10, ignored_exceptions=None):
        return WebDriverWait(self.driver, timeout_sec, ignored_exceptions=ignored_exceptions).until(
            getattr(EC, EXPECTED_CONDITIONS_ELEMENTS.get(expected_condition))(locator),
            message=f"Can't find elements by locator {locator}")

    def click_on(self, locator, timeout_sec=10):
        self.find_element(locator, expected_condition='clickable', timeout_sec=timeout_sec).click()

    def navigate_to(self, url=''):
        url = self.base_url + url
        self.driver.get(url)
        time.sleep(3)

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def enter_txt(self, locator, txt):
        self.find_element(locator).send_keys(txt)

    def wait_until_visibility_of_element_located(self, locator):
        WebDriverWait(self.driver, timeout=5).until(EC.visibility_of_element_located(locator))

    @classmethod
    def select_item_listbox(cls, listbox: list, chain_name: str) -> None:
        for item in listbox:
            if item.text == chain_name:
                item.click()
                break

    def open_listbox(self, locator: object) -> None:
        try:
            self.find_element(locator).click()
        except WebDriverException as e:
            print(e)
            # LOGGER(e)

    def get_listbox(self, open_locator: object, listbox_locator: object) -> list:
        try:
            listbox = self.find_elements(listbox_locator, timeout_sec=2)
        except TimeoutException as e:
            self.open_listbox(open_locator)
            listbox = self.find_elements(listbox_locator, timeout_sec=2)
        return listbox

    def get_valid_listbox(self, open_locator: object, listbox_locator: object, timeout=5) -> list:
        start_time = time.time()
        while time.time() - start_time <= timeout:
            if listbox[0].aria_role == 'none':
                listbox = self.get_listbox(open_locator, listbox_locator)
                time.sleep(1)
            else:
                return listbox


