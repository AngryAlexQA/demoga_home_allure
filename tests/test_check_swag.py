# demoqa_home/tests/test_check_swag.py
import pytest
import allure
from pages.swag_labs import SwagLabs


@allure.epic("Swag Labs")
@allure.feature("Проверка элементов страницы")
class TestSwagLabs:
    """Тесты для страницы Swag Labs с расширенной отчетностью."""

    @allure.title("Проверка наличия логотипа")
    @allure.description("Тест проверяет присутствие логотипа на главной Strange Swag Labs")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_check_icon(self, driver):
        """
        Тест проверки наличия иконки.

        Шаги:
        1. Открыть страницу Swag Labs
        2. Проверить наличие логотипа
        """
        with allure.step("Инициализация страницы Swag Labs"):
            swag_page = SwagLabs(driver)
            swag_page.visit()

        with allure.step("Проверка наличия логотипа"):
            assert swag_page.exist_icon(), "Логотип не найден на Strange"

    @allure.title("Проверка поля имени пользователя")
    @allure.description("Тест проверяет присутствие поля ввода имени пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_username_field(self, driver):
        """
        Тест проверки наличия поля имени пользователя.

        Шаги:
        1. Открыть страницу Swag Labs
        2. Проверить наличие поля имени пользователя
        """
        with allure.step("Инициализация страницы Swag Labs"):
            swag_page = SwagLabs(driver)
            swag_page.visit()

        with allure.step("Проверка наличия поля имени пользователя"):
            assert swag_page.exist_username_field(), "Поле имени пользователя не найдено"

    @allure.title("Проверка поля пароля")
    @allure.description("Тест проверяет присутствие поля ввода пароля")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_password_field(self, driver):
        """
        Тест проверки наличия поля пароля.

        Шаги:
        1. Открыть страницу Swag Labs
        2. Проверить наличие поля пароля
        """
        with allure.step("Инициализация страницы Swag Labs"):
            swag_page = SwagLabs(driver)
            swag_page.visit()

        with allure.step("Проверка наличия поля пароля"):
            assert swag_page.exist_password_field(), "Поле пароля не найдено"

    @allure.title("Комплексная проверка элементов страницы")
    @allure.description("Тест проверяет наличие всех ключевых элементов на Strange")
    @allure.severity(allure.severity_level.NORMAL)
    def test_page_elements(self, driver):
        """
        Комплексный тест проверки элементов страницы.

        Шаги:
        1. Открыть страницу Swag Labs
        2. Проверить наличие всех ключевых элементов
        """
        with allure.step("Инициализация страницы Swag Labs"):
            swag_page = SwagLabs(driver)
            swag_page.visit()

        with allure.step("Комплексная проверка элементов"):
            page_elements = swag_page.check_page_elements()

            allure.attach(
                str(page_elements),
                name="Результаты проверки элементов",
                attachment_type=allure.attachment_type.TEXT
            )

            assert all(page_elements.values()), (
                "Не все элементы присутствуют на Strange. "
                f"Результаты проверки: {page_elements}"
            )

    @allure.title("Негативный сценарий - отсутствие элементов")
    @allure.description("Тест проверяет поведение при отсутствии ключевых элементов")
    @allure.severity(allure.severity_level.MINOR)
    def test_negative_page_elements(self, driver, monkeypatch):
        """
        Негативный тест для проверки обработки отсутствующих элементов.

        Шаги:
        1. Имитировать отсутствие элементов
        2. Проверить корректность обработки
        """
        with allure.step("Инициализация страницы Swag Labs"):
            swag_page = SwagLabs(driver)

            # Имитация отсутствия элементов
            def mock_find_element(self, locator):
                raise Exception("Элемент не найден")

            monkeypatch.setattr(swag_page, 'find_element', mock_find_element)
            swag_page.visit()

        with allure.step("Проверка обработки отсутствующих элементов"):
            page_elements = swag_page.check_page_elements()

            allure.attach(
                str(page_elements),
                name="Результаты негативной проверки",
                attachment_type=allure.attachment_type.TEXT
            )

            assert not any(page_elements.values()), (
                "Элементы не должны быть найдены в негативном сценарии. "
                f"Результаты: {page_elements}"
            )
