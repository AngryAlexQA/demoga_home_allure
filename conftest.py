# demoqa_home/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

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
