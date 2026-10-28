import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Setup and teardown Chrome for every test
@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    yield driver
    driver.quit()


# Wait for alert, read it, and close it
def get_alert_text(driver):
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    return text


# Test 1: Empty username
def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:30080/")

    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()

    alert_text = get_alert_text(driver)

    assert alert_text == "Username cannot be empty."


# Test 2: Empty password
def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:30080/")

    driver.find_element(By.NAME, "username").send_keys("John Doe")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()

    alert_text = get_alert_text(driver)

    assert alert_text == "Password cannot be empty."


# Test 3: Password shorter than 6 characters
def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:30080/")

    driver.find_element(By.NAME, "username").send_keys("Jane")
    driver.find_element(By.NAME, "pwd").send_keys("abc1")
    driver.find_element(By.NAME, "sb").click()

    alert_text = get_alert_text(driver)

    assert alert_text == "Password must be at least 6 characters long."


# Test 4: Valid registration
def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:30080/")

    driver.find_element(By.NAME, "username").send_keys("Alice")
    driver.find_element(By.NAME, "pwd").send_keys("abc123")
    driver.find_element(By.NAME, "sb").click()

    # Wait until Flask redirects to /submit
    WebDriverWait(driver, 10).until(
        EC.url_contains("/submit")
    )

    assert "/submit" in driver.current_url

    # Verify greeting message
    body_text = driver.find_element(By.TAG_NAME, "body").text

    assert "Hello, Alice! Welcome to the website" in body_text