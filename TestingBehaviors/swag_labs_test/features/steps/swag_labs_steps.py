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
