import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from tests.test_setup import TestSetup, pages_fixture
from utils.helpers import parametrize_generator

CONFIG_FILE = "test_config.json"


class TestHomePage(TestSetup):

    @pytest.mark.ui
    @pytest.mark.parametrize(
        *parametrize_generator(CONFIG_FILE, "page_key", "expected_title")
    )
    def test_homepage_title(self, pages_fixture, page_key, expected_title):
        url = pages_fixture[page_key]
        self.driver.get(url)
        assert (
            self.driver.title == expected_title
        ), f"Expected title '{expected_title}' but got '{self.driver.title}'"

    @pytest.mark.login
    @pytest.mark.parametrize(
        *parametrize_generator(CONFIG_FILE, "page_key", "expected_login_redirect")
    )
    def test_redirect_to_login(self, pages_fixture, page_key, expected_login_redirect):
        url = pages_fixture[page_key]
        self.driver.get(url)
        self.driver.implicitly_wait(5)

        current_url = self.driver.current_url
        is_redirected = "login" in current_url or "signin" in current_url

        assert (
            is_redirected == expected_login_redirect
        ), f"Redirection check failed for {url}, expected: {expected_login_redirect}, got: {is_redirected}"

class TestElementLoginPage(TestSetup):

    @pytest.mark.ui
    @pytest.mark.login
    @pytest.mark.parametrize(
        *parametrize_generator(CONFIG_FILE, "page_key", "expected_login")
    )
    def test_login_text_present(self, pages_fixture, page_key, expected_login):

        url = pages_fixture[page_key]
        self.driver.get(url)

        self.driver.implicitly_wait(5)

        try:
            login_element = self.driver.find_element(By.XPATH, "//*[text()='Login']")
            is_present = login_element.is_displayed()
        except NoSuchElementException:
            is_present = False

        assert is_present == expected_login, f"'Login' text presence mismatch on {url}"

    @pytest.mark.login
    @pytest.mark.parametrize(
        *parametrize_generator(
            CONFIG_FILE, "page_key", "username", "password", "failed_message"
        )
    )
    def test_login_functionality(
        self, pages_fixture, page_key, username, password, failed_message
    ):
        self.driver.get(pages_fixture[page_key])

        self.driver.implicitly_wait(5)

        try:
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            submit_button = self.driver.find_element(
                By.XPATH, "//button[@type='submit']"
            )
        except NoSuchElementException:
            assert (
                False
            ), "One of the elements (username, password, or submit button) was not found."

        username_field.send_keys(username)
        password_field.send_keys(password)

        submit_button.click()

        self.driver.implicitly_wait(2)

        try:
            self.driver.find_element(By.XPATH, f"//*[text()='{failed_message}']")
            raise Exception("Login failed!")
        except NoSuchElementException:
            pass
