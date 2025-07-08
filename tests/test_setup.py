import pytest
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

@pytest.fixture(scope="module")
def pages_fixture():
    return {
        "orange": "https://opensource-demo.orangehrmlive.com/web/index.php",
        "google": "https://www.google.com/",
    }


class TestSetup:

    @pytest.fixture(scope="class", autouse=True)
    def setup(self, request):
        session = requests.Session()
        request.cls.session = session
      
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

        driver.maximize_window()

        request.cls.driver = driver
        yield
        driver.quit()
        session.close()
