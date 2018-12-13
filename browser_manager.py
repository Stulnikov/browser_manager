from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Driver():
    @property
    def driver(self) -> WebDriver:
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    @driver.deleter
    def driver(self):
        del self._driver


class Browser(metaclass=Singleton):
    def __init__(self):
        self._driver = Driver()
        self._executable_path = None

    def set_executable_path(self, path):
        self._executable_path = path

    def open_browser(self):
        self._driver.driver = webdriver.Chrome(executable_path=self._executable_path)

    @property
    def driver(self) -> WebDriver:
        return self._driver.driver

    def close_browser(self):
        self._driver.driver.quit()
        del self._driver.driver


class Browsers(metaclass=Singleton):
    def __init__(self):
        self.__active_browser = 1
        self._first_driver = Driver()
        self._second_driver = Driver()
        self._executable_path = None

    def set_executable_path(self, path):
        self._executable_path = path

    def open_browsers(self):
        self.open_first_browser()
        self.open_second_browser()

    def open_first_browser(self):
        self._first_driver.driver = webdriver.Chrome(self._executable_path)

    def open_second_browser(self):
        self._second_driver.driver = webdriver.Chrome(self._executable_path)

    @property
    def driver(self) -> WebDriver:
        if self.__active_browser == 1:
            return self._first_driver.driver
        elif self.__active_browser == 2:
            return self._second_driver.driver

    def switch_to_first_browser(self):
        self.__active_browser = 1

    def switch_to_second_browser(self):
        self.__active_browser = 2

    def close_first_browser(self):
        self._first_driver.driver.quit()
        del self._first_driver.driver

    def close_second_browser(self):
        self._second_driver.driver.quit()
        del self._second_driver.driver

    def close_browsers(self):
        self.close_first_browser()
        self.close_second_browser()
