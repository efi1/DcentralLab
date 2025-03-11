import inspect
import logging
import pytest
from tests.pages.main_page import MainPage

LOGGER = logging.getLogger()


@pytest.fixture(scope='module')
def get_pages_instances(browser, global_data):
    url = global_data.hord_url
    main_page = MainPage(browser, url)
    main_page.navigate_to()
    return main_page.go_to_hord(url), main_page


def verify_result(actual_result, expected_result, err_msg):
    assert actual_result == expected_result, (F"{err_msg}, expected: {expected_result}, "
                                              F"found: {actual_result}")


# @pytest.mark.skip('skipped for developing purposes')
def test_sidebar_verification(browser, get_pages_instances):
    """ Test the sidebar functionality """
    LOGGER.info(F"\n\n++++ in {inspect.currentframe().f_code.co_name}....\n")
    hord, _ = get_pages_instances
    assert hord.is_sidebar_expand is True, F"sidebar is not expanded as expected"
    sidebar_ele = hord.get_action_chains
    hord.toggle_sidebar(sidebar_ele)
    assert hord.is_sidebar_expand is False, F"sidebar is wrongly expanded"
    hord.toggle_sidebar(sidebar_ele)
    assert hord.is_sidebar_expand is True, F"sidebar is not expanded as expected"
    LOGGER.info(F"sidebar verification completed successfully")


def test_faq_titles_verification(test_data, get_pages_instances):
    """  Verify the correctness of the faq's titles """
    LOGGER.info(F"\n\n++++ in {inspect.currentframe().f_code.co_name}....")
    hord, _ = get_pages_instances
    faq_items = hord.get_faq_items
    faq_text_items = hord.verify_faq_titles(faq_items)
    verify_result(faq_text_items, test_data.faq_items, 'wrong titles content')
    LOGGER.info(F"faq titles verification completed successfully")


def test_verify_links_functionality(browser, get_pages_instances):
    """ Verify that all links are clickable """
    LOGGER.info(F"\n\n++++ in {inspect.currentframe().f_code.co_name}....")
    hord, main_page = get_pages_instances
    main_page.go_bottom
    is_clickable = hord.verify_links_functionality
    verify_result(is_clickable, True, 'faq links are not clickable')


def test_faq_links_answers(browser, test_data, get_pages_instances):
    """ Verify the correctness of all links' answers """
    LOGGER.info(F"\n\n++++ in {inspect.currentframe().f_code.co_name}....")
    hord, main_page = get_pages_instances
    faq_items = hord.get_faq_items
    main_page.go_bottom
    links_content = hord.verify_faq_answer_links(faq_items)
    verify_result(links_content, test_data.faq_links_content, 'wrong links answer')
    LOGGER.info(F"++++ faq links answers verification succeeded")


def test_verify_airdrops_content(browser, test_data, get_pages_instances):  # Bonus question
    """ Verify that the content in last airdrops container is correct """
    LOGGER.info(F"\n\n++++ in {inspect.currentframe().f_code.co_name}....")
    hord, main_page = get_pages_instances
    main_page.go_up
    hord.click_on_revenue_share()
    actual_airdrops_content = hord.get_revenue_content
    expected_airdrops_content = test_data.last_airdrops_content
    verify_result(actual_airdrops_content, expected_airdrops_content, 'airdrops content is not as expected')
    LOGGER.info(F"++++ last airdrops container content verification succeeded")
