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


@when("I refresh the Swag Labs login page")
def step_refresh_swag_labs_login_page(context):
    context.behave_driver.refresh()
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


@then("the Swag Labs login fields should be empty")
def step_swag_labs_login_fields_empty(context):
    driver = context.behave_driver
    username = driver.find_element(By.CSS_SELECTOR, "[data-test='username']")
    password = driver.find_element(By.CSS_SELECTOR, "[data-test='password']")
    assert username.get_attribute("value") == ""
    assert password.get_attribute("value") == ""


@then('the Swag Labs username field should prompt "{prompt}"')
def step_swag_labs_username_prompt(context, prompt):
    username = context.behave_driver.find_element(
        By.CSS_SELECTOR, "[data-test='username']"
    )
    assert username.get_attribute("placeholder") == prompt


@then("the Swag Labs password field should mask what I type")
def step_swag_labs_password_field_masks_input(context):
    password = context.behave_driver.find_element(
        By.CSS_SELECTOR, "[data-test='password']"
    )
    assert password.get_attribute("type") == "password"


@then('the Swag Labs password field should prompt "{prompt}"')
def step_swag_labs_password_prompt(context, prompt):
    password = context.behave_driver.find_element(
        By.CSS_SELECTOR, "[data-test='password']"
    )
    assert password.get_attribute("placeholder") == prompt


@then("the Swag Labs login button should be enabled")
def step_swag_labs_login_button_enabled(context):
    login_button = context.behave_driver.find_element(
        By.CSS_SELECTOR, "[data-test='login-button']"
    )
    assert login_button.is_enabled()
