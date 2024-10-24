from tests.pages.main_page import MainPage


def test_select_farm_token(browser, root_url, load_test_config):
    chain_name = load_test_config['test_staging']['chain_name']
    main_page = MainPage.navigate(browser, root_url)
    selected_item = main_page.select_from_chains_dropdown(chain_name)
    assert selected_item == chain_name, F"item wrongly selected; {selected_item} instead of {chain_name}"

