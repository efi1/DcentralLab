import time

import pytest
from tests.pages.main_page import MainPage


def test_sidebar_verification(browser, global_data):
    url = global_data.hord_url
    main_page = MainPage(browser, url)
    hord = main_page.go_to_hord(url)
    main_page.navigate_to()
    assert hord.is_sidebar_expand is True, F"sidebar is not expanded as expected"
    hord.toggle_sidebar
    assert hord.is_sidebar_expand is False, F"sidebar is wrongly expanded"
    hord.toggle_sidebar
    assert hord.is_sidebar_expand is True, F"sidebar is not expanded as expected"


# @pytest.mark.skip('temp')
def test_text_faq(browser, test_config):
    url = test_config.url
    main_page = MainPage(browser, url)
    hord = main_page.go_to_hord(url)
    main_page.navigate_to()
    faq_items = hord.get_faq_items
    faq_text_items = hord.verify_faq_titles(faq_items)
    assert test_config.faq_items == faq_text_items, (F"faq are not as expected, expected: {test_config.faq_items}, "
                                                     F"found: {faq_text_items}")


# @pytest.mark.skip('temp')
def test_faq_links(browser, test_config):
    url = test_config.url
    main_page = MainPage(browser, url)
    hord = main_page.go_to_hord(url)
    main_page.navigate_to()
    faq_items = hord.get_faq_items
    main_page.go_bottom
    is_clickable, links_content = hord.verify_faq_links(faq_items)
    assert is_clickable is True, "faq links are not clickable"
    assert links_content == test_config.faq_links_content
