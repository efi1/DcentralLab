import inspect
import logging
import pytest
from tests.pages.main_page import MainPage

LOGGER = logging.getLogger()


# @pytest.mark.skip('temp')
def test_sidebar_verification(browser, global_data):
    """ Test the sidebar functionality """
    LOGGER.info(F"\n\n++++ in {inspect.currentframe().f_code.co_name}....")
    url = global_data.hord_url
    main_page = MainPage(browser, url)
    hord = main_page.go_to_hord(url)
    main_page.navigate_to()
    assert hord.is_sidebar_expand is True, F"sidebar is not expanded as expected"
    hord.toggle_sidebar
    assert hord.is_sidebar_expand is False, F"sidebar is wrongly expanded"
    hord.toggle_sidebar
    assert hord.is_sidebar_expand is True, F"sidebar is not expanded as expected"
    LOGGER.info(F"sidebar verification completed successfully")


# @pytest.mark.skip('temp')
def test_faq_titles_verification(browser, test_config):
    """  Verify the correctness of the faq's titles """
    LOGGER.info(F"\n\n++++ in {inspect.currentframe().f_code.co_name}....")
    url = test_config.url
    main_page = MainPage(browser, url)
    hord = main_page.go_to_hord(url)
    main_page.navigate_to()
    faq_items = hord.get_faq_items
    faq_text_items = hord.verify_faq_titles(faq_items)
    assert test_config.faq_items == faq_text_items, (F"faq are not as expected, expected: {test_config.faq_items}, "
                                                     F"found: {faq_text_items}")
    LOGGER.info(F"faq text verification completed successfully")


# @pytest.mark.skip('temp')
def test_faq_links_answers(browser, test_config):
    """ Verify the correctness of all links' answers """
    LOGGER.info(F"\n\n++++ in {inspect.currentframe().f_code.co_name}....")
    url = test_config.url
    main_page = MainPage(browser, url)
    hord = main_page.go_to_hord(url)
    main_page.navigate_to()
    faq_items = hord.get_faq_items
    main_page.go_bottom
    links_content = hord.verify_faq_answer_links(faq_items)
    assert links_content == test_config.faq_links_content
    LOGGER.info(F"++++ faq links answers verification succeeded")


# @pytest.mark.skip('temp')
def test_verify_links_functionality(browser, global_data):
    """ Verify that all links are clickable """
    url = global_data.hord_url
    main_page = MainPage(browser, url)
    hord = main_page.go_to_hord(url)
    main_page.navigate_to()
    main_page.go_bottom
    is_clickable = hord.verify_links_functionality
    assert is_clickable is True, "faq links are not clickable"
