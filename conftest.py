# demoqa_home/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import allure
from datetime import datetime


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            # Получаем драйвер из фикстуры
            driver = item.funcargs['driver']

            # Создаем скриншот
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f'screenshot_{datetime.now().strftime"%Y%m%d_%H%M%S")}',
                attachment_type=
            allure.attachment_type.PNG
            )
            except Exception as e:
            print(f"Не удалось создать скриншот: {e}")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def driver():
    # Настройки Chrome для CI/CD
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Для запуска в CI
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-extensions')
    
    # Автоматическая установка ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    logger.info("WebDriver инициализирован")
    yield driver

    # Закрытие драйвера после теста
    driver.quit()
    logger.info("WebDriver закрыт")
