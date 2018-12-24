from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Driver():
    def __init__(self):
        self.__driver = None

    @property
    def driver(self) -> WebDriver:
        if not self.__driver:
            raise WebDriverException('The browser is not open')
        return self.__driver

    @driver.setter
    def driver(self, web_driver: WebDriver):
        def close_browsers_with_exception(message):
            try:
                self.__driver.quit()
                web_driver.quit()
            except:
                pass
            raise WebDriverException(message)

        if not isinstance(web_driver, WebDriver):
            close_browsers_with_exception('The attribute passed must be WebDriver')

        if self.__driver:
            close_browsers_with_exception('The browser is already open')

        self.__driver = web_driver

    @driver.deleter
    def driver(self):
        self.__driver = None


class BaseBrowser():
    def __init__(self):
        self.__driver = Driver()

    def open_browser(self, driver):
        self.__driver.driver = driver

    @property
    def driver(self) -> WebDriver:
        return self.__driver.driver

    def close_browser(self):
        self.__driver.driver.quit()
        del self.__driver.driver


class Browser(BaseBrowser, metaclass=Singleton):
    def __init__(self):
        super().__init__()


class Browsers(metaclass=Singleton):
    def __init__(self):
        self.__active_browser = 1
        self.__first_browser = BaseBrowser()
        self.__second_browser = BaseBrowser()

    def open_browsers(self, first_driver, second_driver):
        self.open_first_browser(first_driver)
        self.open_second_browser(second_driver)

    def open_first_browser(self, driver):
        self.__first_browser.open_browser(driver)

    def open_second_browser(self, driver):
        self.__second_browser.open_browser(driver)

    @property
    def driver(self) -> WebDriver:
        if self.__active_browser == 1:
            return self.__first_browser.driver
        elif self.__active_browser == 2:
            return self.__second_browser.driver

    def switch_to_first_browser(self):
        self.__active_browser = 1

    def switch_to_second_browser(self):
        self.__active_browser = 2

    def close_first_browser(self):
        self.__first_browser.driver.quit()

    def close_second_browser(self):
        self.__second_browser.driver.quit()

    def close_browsers(self):
        self.close_first_browser()
        self.close_second_browser()
