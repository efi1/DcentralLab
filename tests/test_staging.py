import inspect
import logging
import pytest
from tests.pages.main_page import MainPage

LOGGER = logging.getLogger()


@pytest.mark.parametrize("search_type", ['css', 'xpath'])
def test_select_farm_token(browser, test_config, search_type):
    LOGGER.info(F"\n\n++++ in {inspect.currentframe().f_code.co_name}....")
    chain_name = test_config.chain_name
    url_list = test_config.url_list
    main_page = MainPage(browser, url_list)
    staging = main_page.go_to_staging(search_type)
    main_page.navigate_to(page_displayed=staging.locators.page_displayed)
    main_page.go_bottom
    staging.open_listbox
    listbox = staging.get_listbox()
    staging.select_item_listbox(listbox, chain_name)
    selected_item = staging.get_selected_item
    assert selected_item == chain_name, F"item wrongly selected; {selected_item} instead of {chain_name}"
    LOGGER.info(F"selecting farm token by css and xpath completed successfully")
