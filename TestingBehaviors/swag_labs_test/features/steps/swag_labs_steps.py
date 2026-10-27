from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


@given("I open Swag Labs")
def step_open_swag_labs(context):
    context.behave_driver.get("https://www.saucedemo.com/")
    WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='login-button']"))
    )


@then('the Swag Labs page title should be "{title}"')
def step_swag_labs_page_title(context, title):
    assert context.behave_driver.title == title


@then("the Swag Labs login form should be ready")
def step_swag_labs_login_form_ready(context):
    driver = context.behave_driver
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='username']"))
    )
    assert driver.find_element(
        By.CSS_SELECTOR, "[data-test='password']"
    ).is_displayed()
    assert driver.find_element(
        By.CSS_SELECTOR, "[data-test='login-button']"
    ).is_displayed()
