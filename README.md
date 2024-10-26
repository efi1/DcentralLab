# DcentralLab

The goal of this assignment (project) is to write a Python script that automates tasks on Staging and Hord pages, 
covering both UI testing using Selenium.

This solution has two test files - test_hord.py and test_staging.py.
These files and all relevant code resides under tests' folder.

The pages' clients resides under test.pages and contains the code which both tests use.
It consists on the Page Object Model approach, in which each group of activities is gathered at its own page 
(i.e hord_page.py contains all activities which relevant to hord page verification.)

Locators which are being used by both pages resides under tests.utils.locators.py file.

Global and tests configuration files resides under tests.config folder.
They used for test data and configuration as well for the browser configuration.

Tests are running under the pytest work frame.
it has a conftest.py file (under tests folder) which initiate the webdriver as well as calls for tearDown in the end.

You may select your desired browser; Chrome, Firefox or Edge.
To do so, you should update the browser field in global_config.cfg (under tests.config) with your desired browser.

Test's cfg files (resides under tests.config.cfg_tests) and contains the specific data for the test.


## Before running the tests:
  - Create a Python virtual environment and activate it.
  - upgrade the pip package by: **python -m pip install --upgrade pip**
  - install setup.py by: **python -m setup.py install**


## To run the tests via pytest (for both Windows and Linux)
- First, install the setup.py as mentioned above 
- To run the test via cli, while being in the **project's root tree**, type (and virtualenv is activated):
  **python -m pytest**


## Log files
Are written to the logs folder which is under the tree root.

