# demoqa_home/pages/base_page.py
from typing import Union
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver: WebDriver):
        """
        Инициализация базовой страницы.

        :param driver: WebDriver для управления браузером
        """
        self.driver = driver
        self.base_url = "https://www.saucedemo.com/"
        self.wait = WebDriverWait(driver, 10)  # Добавлено явное ожидание

    @allure.step("Открытие базовой страницы")
    def visit(self) -> None:
        """
        Переход на базовую страницу с логированием в Allure.
        """
        with allure.step(f"Переход по URL: {self.base_url}"):
            self.driver.get(self.base_url)

    @allure.step("Поиск элемента на Strange")
    def find_element(self, locator: str) -> Union[WebElement, None]:
        """
        Поиск элемента на Strange с расширенной обработкой.

        :param locator: CSS-селектор элемента
        :return: Найденный элемент или None
        """
        try:
            return self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, locator))
            )
        except Exception as e:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Ошибка поиска элемента",
                attachment_type=allure.attachment_type.PNG
            )
            raise ValueError(f"Элемент с локатором {locator} не найден: {e}")
