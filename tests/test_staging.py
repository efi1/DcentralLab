import pytest
from tests.pages.main_page import MainPage


@pytest.mark.parametrize("search_type", ['css', 'xpath'])
# @pytest.mark.skip('tmp')
def test_select_farm_token(browser, test_config, search_type):
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

