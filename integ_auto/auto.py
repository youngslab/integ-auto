
# web driver
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# web element
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# wait elements
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# multi-dispatch
from plum import dispatch  # mulitple dispatch
from typing import Tuple, Union, List

_default_timeout = 60


def get_clickable(driver: WebDriver, by: str, path: str, timeout: int = _default_timeout) -> Union[WebElement, None]:
    try:
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, path)))
    except Exception as e:
        return None


def get_element(driver: WebDriver, by: str, path: str, timeout: int = _default_timeout) -> Union[WebElement, None]:
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, path)))
    except Exception as e:
        return None


def get_elements(driver: WebDriver, by: str, path: str, timeout: int = _default_timeout) -> List[WebElement]:
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((by, path)))
    except Exception as e:
        return []


def click(driver: WebDriver, element: WebElement):
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)


def type(element: WebElement, text: str):
    element.clear()
    if element.get_attribute('value'):
        return False
    element.send_keys(text)
    return True


def select(element: WebElement, text: str):
    select = Select(element)
    select.select_by_visible_text(text)
    return True


class Frame:
    def __init__(self, driver, element: WebElement, timeout=_default_timeout):
        self.driver = driver
        self.frame = element

    def __enter__(self):
        self.driver.switch_to.frame(self.frame)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.switch_to.parent_frame()


class Automatic:

    def create_edge_driver(*, headless=False):
        options = webdriver.EdgeOptions()
        options.add_argument('log-level=3')
        if headless:
            options.add_argument('headless')
            options.add_argument('disable-gpu')
        service = Service(EdgeChromiumDriverManager().install())
        return webdriver.Edge(options=options, service=service)

    def __init__(self, driver: WebDriver, *, timeout=60):
        self.driver = driver
        self.timeout = timeout

    def go(self, url: str):
        return self.driver.get(url)

    @dispatch
    def get_element(self, by: str, path: str, *, timeout: int = _default_timeout) -> Union[WebElement, None]:
        return get_element(self.driver, by, path, timeout)

    @dispatch
    def get_elements(self, by: str, path: str, *, timeout: int = _default_timeout) -> List[WebElement]:
        return get_elements(self.driver, by, path, timeout)

    def get_clickable(self, by: str, path: str, *, timeout: int = _default_timeout) -> Union[WebElement, None]:
        return get_clickable(self.driver, by, path, timeout)

    def select(self, element: WebElement, text: str):
        return select(element, text)

    @dispatch
    def type(self, element: WebElement, text: str):
        return type(element, text)

    @dispatch
    def click(self, element: WebElement):
        return click(self.driver, element)

    @dispatch
    def get_frame(self, element: WebElement):
        if not element:
            return None
        return Frame(self.driver, element)
