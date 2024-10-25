import pytest
from tests.pages.main_page import MainPage


def test_expanded_sidebar(browser, test_config):
    url = test_config.url
    main_page = MainPage(browser, url)
    hord = main_page.go_to_hord(url)
    main_page.navigate_to()
    assert hord.is_sidebar_expand is True, F"sidebar is not expanded as expected"
    hord.toggle_sidebar
    assert hord.is_sidebar_expand is False, F"sidebar is wrongly expanded"
    hord.toggle_sidebar
    assert hord.is_sidebar_expand is True, F"sidebar is not expanded as expected"
