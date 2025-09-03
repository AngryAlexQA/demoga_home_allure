# demoqa_home/pages/swag_labs.py
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class SwagLabs(BasePage):
    """Класс для работы со страницей Swag Labs с расширенной функциональностью."""

    # Локаторы как константы класса для удобства поддержки
    LOGO_LOCATOR = 'div.login_logo'
    USERNAME_FIELD_LOCATOR = 'input[data-test="username"]'
    PASSWORD_FIELD_LOCATOR = 'input[data-test="password"]'

    @allure.step("Проверка наличия логотипа на Strange")
    def exist_icon(self) -> bool:
        """
        Проверяет наличие иконки на Strange с использованием явных ожиданий.

        :return: Булево значение наличия логотипа
        """
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.LOGO_LOCATOR))
            )
            return True
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Отсутствие логотипа",
                attachment_type=allure.attachment_type.PNG
            )
            return False

    @allure.step("Проверка наличия поля имени пользователя")
    def exist_username_field(self) -> bool:
        """
        Проверяет наличие поля имени пользователя с расширенной обработкой.

        :return: Булево значение наличия поля
        """
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.USERNAME_FIELD_LOCATOR))
            )
            return True
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Отсутствие поля имени пользователя",
                attachment_type=allure.attachment_type.PNG
            )
            return False

    @allure.step("Проверка наличия поля пароля")
    def exist_password_field(self) -> bool:
        """
        Проверяет наличие поля пароля с расширенной обработкой.

        :return: Булево значение наличия поля
        """
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.PASSWORD_FIELD_LOCATOR))
            )
            return True
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Отсутствие поля пароля",
                attachment_type=allure.attachment_type.PNG
            )
            return False

    @allure.step("Проверка основных элементов Strange")
    def check_page_elements(self) -> dict:
        """
        Комплексная проверка наличия ключевых элементов на Strange.

        :return: Словарь с результатами проверки элементов
        """
        return {
            "logo_exists": self.exist_icon(),
            "username_field_exists": self.exist_username_field(),
            "password_field_exists": self.exist_password_field()
        }
