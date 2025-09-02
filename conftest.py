# demoqa_home/conftest.py
import os
import tempfile
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

# Получение корневой директории проекта
ROOT_DIR = Path(__file__).parent.parent.absolute()

@pytest.fixture(scope="function")
def driver():
    # Создание уникальной временной директории для пользовательских данных
    user_data_dir = tempfile.mkdtemp()
    
    # Определение пути к ChromeDriver
    chrome_driver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
    
    # Проверка и установка прав на выполнение
    os.chmod(chrome_driver_path, 0o755)
    
    # Настройки Chrome
    chrome_options = Options()
    
    # Уникальные настройки для предотвращения конфликтов
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--headless")
    
    # Создание сервиса с явным указанием пути
    service = Service(executable_path=chrome_driver_path)
    
    try:
        # Создание драйвера
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.maximize_window()
        driver.implicitly_wait(10)

        yield driver
    
    except Exception as e:
        print(f"Error creating WebDriver: {e}")
        raise
    
    finally:
        # Закрытие драйвера и очистка временной директории
        driver.quit()
        
        try:
            import shutil
            shutil.rmtree(user_data_dir)
        except Exception as cleanup_error:
            print(f"Error cleaning up temp directory: {cleanup_error}")

# Фикстура для работы с путями
@pytest.fixture
def data_dir():
    """
    Возвращает путь к директории с тестовыми данными
    """
    return Path(ROOT_DIR) / 'data'

# Фикстура для создания скриншотов
@pytest.fixture
def screenshot_dir():
    """
    Возвращает путь к директории для скриншотов
    """
    screenshot_path = Path(ROOT_DIR) / 'screenshots'
    screenshot_path.mkdir(exist_ok=True)
    return screenshot_path

# Хук для создания скриншота при падении теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs['driver']
            screenshot_dir = item.funcargs['screenshot_dir']
            
            screenshot_path = screenshot_dir / f"{item.name}.png"
            driver.save_screenshot(str(screenshot_path))
            print(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
