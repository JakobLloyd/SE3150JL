from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


LOGIN_URL = "https://www.saucedemo.com"
USERNAME = (By.CSS_SELECTOR, "[data-test='username']")
PASSWORD = (By.CSS_SELECTOR, "[data-test='password']")
LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test='login-button']")
LOGIN_ERROR = (By.CSS_SELECTOR, "[data-test='error']")


@given("I open Swag Labs")
def step_open_swag_labs(context):
    context.behave_driver.get(LOGIN_URL)
    WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located(LOGIN_BUTTON)
    )


@when("I refresh the Swag Labs login page")
def step_refresh_swag_labs_login_page(context):
    context.behave_driver.refresh()
    WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located(LOGIN_BUTTON)
    )


@when('I enter "{username}" as my Swag Labs username')
def step_enter_swag_labs_username(context, username):
    context.behave_driver.find_element(*USERNAME).send_keys(username)


@when('I enter "{password}" as my Swag Labs password')
def step_enter_swag_labs_password(context, password):
    context.behave_driver.find_element(*PASSWORD).send_keys(password)


@when("I submit the Swag Labs login form")
def step_submit_swag_labs_login_form(context):
    context.behave_driver.find_element(*LOGIN_BUTTON).click()


@when("I submit the Swag Labs login form by pressing Enter")
def step_submit_swag_labs_login_form_with_enter(context):
    context.behave_driver.find_element(*PASSWORD).send_keys(Keys.ENTER)


@when("I dismiss the Swag Labs login message")
def step_dismiss_swag_labs_login_message(context):
    driver = context.behave_driver
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located(LOGIN_ERROR))
    driver.find_element(By.CSS_SELECTOR, "[data-test='error-button']").click()
    WebDriverWait(driver, 15).until(EC.invisibility_of_element_located(LOGIN_ERROR))


@when("I clear the Swag Labs username field")
def step_clear_swag_labs_username(context):
    context.behave_driver.find_element(*USERNAME).clear()


@then('the Swag Labs page title should be "{title}"')
def step_swag_labs_page_title(context, title):
    assert context.behave_driver.title == title


@then("the Swag Labs login form should be ready")
def step_swag_labs_login_form_ready(context):
    driver = context.behave_driver
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located(USERNAME))
    assert driver.find_element(*PASSWORD).is_displayed()
    assert driver.find_element(*LOGIN_BUTTON).is_displayed()


@then("the Swag Labs login fields should be empty")
def step_swag_labs_login_fields_empty(context):
    driver = context.behave_driver
    assert driver.find_element(*USERNAME).get_attribute("value") == ""
    assert driver.find_element(*PASSWORD).get_attribute("value") == ""


@then('the Swag Labs username field should prompt "{prompt}"')
def step_swag_labs_username_prompt(context, prompt):
    assert context.behave_driver.find_element(*USERNAME).get_attribute(
        "placeholder"
    ) == prompt


@then('the Swag Labs password field should prompt "{prompt}"')
def step_swag_labs_password_prompt(context, prompt):
    assert context.behave_driver.find_element(*PASSWORD).get_attribute(
        "placeholder"
    ) == prompt


@then("the Swag Labs password field should mask what I type")
def step_swag_labs_password_masks_input(context):
    password_type = context.behave_driver.find_element(*PASSWORD).get_attribute("type")
    assert password_type == "password"


@then("the Swag Labs login button should be enabled")
def step_swag_labs_login_button_enabled(context):
    assert context.behave_driver.find_element(*LOGIN_BUTTON).is_enabled()


@then('the Swag Labs username field should contain "{username}"')
def step_swag_labs_username_contains(context, username):
    assert context.behave_driver.find_element(*USERNAME).get_attribute(
        "value"
    ) == username


@then('the Swag Labs password field should contain "{password}"')
def step_swag_labs_password_contains(context, password):
    assert context.behave_driver.find_element(*PASSWORD).get_attribute(
        "value"
    ) == password


@then("the Swag Labs username field should be empty")
def step_swag_labs_username_empty(context):
    assert context.behave_driver.find_element(*USERNAME).get_attribute("value") == ""


@then("the Swag Labs password field should be empty")
@then("the Swag Labs password field should still be empty")
def step_swag_labs_password_empty(context):
    assert context.behave_driver.find_element(*PASSWORD).get_attribute("value") == ""


@then('the Swag Labs login message should say "{message}"')
def step_swag_labs_login_message(context, message):
    error = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located(LOGIN_ERROR)
    )
    assert error.text == message


@then("the Swag Labs login message should be dismissed")
def step_swag_labs_login_message_dismissed(context):
    assert not context.behave_driver.find_elements(*LOGIN_ERROR)


@then("the Swag Labs login page should remain open")
def step_swag_labs_login_page_remains_open(context):
    driver = context.behave_driver
    assert driver.current_url.rstrip("/") == LOGIN_URL
    assert driver.find_element(*LOGIN_BUTTON).is_displayed()
