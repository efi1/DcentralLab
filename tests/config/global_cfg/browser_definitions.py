from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

WEBDRIVER_MANAGER = {'Chrome': ChromeDriverManager, 'Firefox': GeckoDriverManager, 'Edge': EdgeChromiumDriverManager}
BROWSER_SERVICE = {'Chrome': ChromeService, 'Firefox': FirefoxService, 'Edge': EdgeService}
WEBDRIVER_TYPE = {'Chrome': 'chromedriver', 'Firefox': 'geckodriver', 'Edge': 'msedgedriver'}
OPTIONS_TYPE = {'Chrome': 'ChromeOptions', 'Firefox': 'FirefoxOptions', 'Edge': 'EdgeOptions'}





