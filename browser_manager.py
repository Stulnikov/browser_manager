from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BrowserManager(metaclass=Singleton):
    __browsers = {}
    __default_browser = None

    def open_browser(self, web_driver: WebDriver, browser_name='default'):
        if not isinstance(web_driver, WebDriver):
            self._close_browsers_with_exception('The attribute passed must be WebDriver')

        if browser_name in self.__browsers:
            self.__browsers['duplicate'] = web_driver
            self._close_browsers_with_exception('The browser with name: "{}" is already open'.format(browser_name))

        self.__browsers[browser_name] = web_driver
        self.__default_browser = browser_name

    @property
    def driver(self) -> WebDriver:
        if not self.__browsers:
            raise WebDriverException('The browser is not open')

        return self.__browsers[self.__default_browser]

    def switch_to(self, browser_name):
        if browser_name not in self.__browsers:
            self._close_browsers_with_exception('The browser with name: "{}" is not open'.format(browser_name))

        self.__default_browser = browser_name

    def close_browsers(self):
        [self.__browsers.pop(i).quit() for i in list(self.__browsers) if self.__browsers]

    def _close_browsers_with_exception(self, message):
        self.close_browsers()
        raise WebDriverException(message)
