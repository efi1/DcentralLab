import json
import shutil
from pathlib import Path
import pytest as pytest
import yaml
from selenium import webdriver
from jinja2 import Environment, FileSystemLoader
from tests.utils.dict_to_obj import dict_to_obj
from tests.config.global_cfg.browser_definitions import *

DRIVERS_DIR = Path().absolute().joinpath('tests', 'drivers')
GLOBAL_DIRECTORY = Path().absolute().joinpath('tests', 'config', 'global_cfg')
GLOBAL_CONFIG_FILE = Path(GLOBAL_DIRECTORY).joinpath('global_config.cfg')
TEMPLATE_DIR = Path().absolute().joinpath('tests', 'config', 'cfg_tests')


@pytest.fixture
def test_name(request):
    test_name = request.node.name
    return test_name


def read_file(file_path: str):
    with open(file_path, 'r') as f:
        data = f.read()
    return data


def json_load(path) -> json:
    data = read_file(path)
    return json.loads(data)


@pytest.fixture(scope="session")
def global_dict_data(file=GLOBAL_CONFIG_FILE):
    return json_load(file)


@pytest.fixture(scope="session")
def global_data(global_dict_data):
    return dict_to_obj(global_dict_data)


def get_cfg_template(test_name, cfg_template_dir):
    template_loader = FileSystemLoader(searchpath=cfg_template_dir)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(f'{test_name}.cfg')
    return template


@pytest.fixture(scope="function")
def test_data(test_name: str, global_dict_data: dict) -> dict:
    """
    updates test's data with the global_cfg data
    :param test_name: test name
    :param global_data: project's global_cfg data
    :return: updated required test's data
    """
    test_name = test_name.split('[')[0]
    cfg_name = F'{test_name}.cfg'
    cfg_template_file = Path(TEMPLATE_DIR).joinpath(cfg_name)
    if cfg_template_file.exists():
        test_template = get_cfg_template(test_name, TEMPLATE_DIR)
    else:
        return {}
    yaml_data = test_template.render(global_dict_data)
    dict_data = yaml.safe_load(yaml_data)
    return dict_to_obj(dict_data)


@pytest.fixture(scope="module")
def browser_config(global_dict_data):
    browser_config_fn = global_dict_data.get('browser_config')
    browser_template = get_cfg_template(browser_config_fn, GLOBAL_DIRECTORY)
    yaml_data = browser_template.render(global_dict_data)
    return dict_to_obj(yaml.safe_load(yaml_data))


def set_options(opts, browser_config):
    if 'Headless' in browser_config.modes:
        opts.add_argument('--headless=new')
        opts.add_argument('ignore-certificate-errors')
    if 'Silent' in browser_config.modes:
        opts.add_argument('--silent=new')
    if browser_config.window_size == 'Maximized':
        opts.add_argument('--start-maximized=new')
    opts.page_load_strategy = browser_config.page_load_strategy


def get_webdriver(config: object, b_type: str) -> object:
    """
    Initiate and return the driver
    :param config:
    :param b_type: browser type e.g. Chrome, Edge, Firefox
    :return: driver object
    """
    opts = getattr(webdriver, OPTIONS_TYPE[b_type])()
    set_options(opts, config)
    service = BROWSER_SERVICE[b_type]
    driver_manager = WEBDRIVER_MANAGER[b_type]
    driver_fn = WEBDRIVER_TYPE[b_type]
    Path(DRIVERS_DIR).mkdir(parents=True, exist_ok=True)
    """
    Path(DRIVERS_DIR).mkdir(parents=True, exist_ok=True);
    If parents is true, any missing parents of this path are created as needed; 
    they are created with the default permissions without taking mode into account (mimicking the POSIX mkdir -p command).
    If exist_ok is true, FileExistsError will not be raised unless the given path already exists in the file system and 
    is not a directory (same behavior as the POSIX mkdir -p command).
    """
    driver_path = Path(DRIVERS_DIR).joinpath(F"{driver_fn}.exe")
    if driver_path.exists():
        cur_service = service(driver_path)
        driver = getattr(webdriver, b_type)(service=cur_service, options=opts)
    else:
        driver = getattr(webdriver, b_type)(service=service(driver_manager().install()), options=opts)
        shutil.copy(driver.service.path, driver_path)
    return driver


@pytest.fixture(scope="module")
def browser(request, browser_config):
    b_type = browser_config.browser
    if b_type in ['Firefox', 'Chrome', 'Edge']:
        driver = get_webdriver(browser_config, b_type)
    else:
        raise Exception(f'Unknown type of browser')
    driver.implicitly_wait(browser_config.implicit_wait)
    yield driver
    driver.quit()

