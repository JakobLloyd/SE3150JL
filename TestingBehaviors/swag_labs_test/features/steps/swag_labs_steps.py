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


@when("I sign in to browse the Swag Labs catalog")
def step_sign_in_to_swag_labs_catalog(context):
    driver = context.behave_driver
    driver.find_element(By.CSS_SELECTOR, "[data-test='username']").send_keys(
        "standard_user"
    )
    driver.find_element(By.CSS_SELECTOR, "[data-test='password']").send_keys(
        "secret_sauce"
    )
    driver.find_element(By.CSS_SELECTOR, "[data-test='login-button']").click()
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-test='inventory-container']")
        )
    )


@when("I sort the Swag Labs catalog from cheapest to priciest")
def step_sort_catalog_by_ascending_price(context):
    sort_menu = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-test='product-sort-container']")
        )
    )
    Select(sort_menu).select_by_visible_text("Price (low to high)")


@when('I inspect the Swag Labs product "{product_name}"')
def step_inspect_swag_labs_product(context, product_name):
    products = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-test='inventory-item']")
        )
    )
    for product in products:
        name = product.find_element(
            By.CSS_SELECTOR, "[data-test='inventory-item-name']"
        )
        if name.text == product_name:
            name.click()
            WebDriverWait(context.behave_driver, 15).until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "[data-test='inventory-item-name']"),
                    product_name,
                )
            )
            return
    raise AssertionError(f"Swag Labs catalog does not contain {product_name!r}")


@when('I add the Swag Labs product "{product_name}" to my cart')
def step_add_swag_labs_product_to_cart(context, product_name):
    products = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-test='inventory-item']")
        )
    )
    for product in products:
        name = product.find_element(
            By.CSS_SELECTOR, "[data-test='inventory-item-name']"
        )
        if name.text == product_name:
            product.find_element(By.TAG_NAME, "button").click()
            return
    raise AssertionError(f"Swag Labs catalog does not contain {product_name!r}")


@when('I remove the Swag Labs product "{product_name}" from my cart')
def step_remove_swag_labs_product_from_cart(context, product_name):
    products = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-test='inventory-item']")
        )
    )
    for product in products:
        name = product.find_element(
            By.CSS_SELECTOR, "[data-test='inventory-item-name']"
        )
        if name.text == product_name:
            product.find_element(By.TAG_NAME, "button").click()
            return
    raise AssertionError(f"Swag Labs catalog does not contain {product_name!r}")


@when("I open my Swag Labs cart")
def step_open_swag_labs_cart(context):
    context.behave_driver.find_element(
        By.CSS_SELECTOR, "[data-test='shopping-cart-link']"
    ).click()
    WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='cart-list']"))
    )


@when("I continue shopping from my Swag Labs cart")
def step_continue_shopping_from_swag_labs_cart(context):
    context.behave_driver.find_element(
        By.CSS_SELECTOR, "[data-test='continue-shopping']"
    ).click()
    WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-test='inventory-container']")
        )
    )


@when("I begin checkout from my Swag Labs cart")
def step_begin_swag_labs_checkout(context):
    context.behave_driver.find_element(
        By.CSS_SELECTOR, "[data-test='checkout']"
    ).click()
    WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='firstName']"))
    )


@then("Swag Labs should ask for my checkout details")
def step_swag_labs_checkout_details_form(context):
    driver = context.behave_driver
    heading = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='title']"))
    )
    assert heading.text == "Checkout: Your Information"
    assert driver.find_element(By.CSS_SELECTOR, "[data-test='firstName']").is_displayed()
    assert driver.find_element(By.CSS_SELECTOR, "[data-test='lastName']").is_displayed()
    assert driver.find_element(By.CSS_SELECTOR, "[data-test='postalCode']").is_displayed()


@then("my Swag Labs cart should contain {count:d} item")
@then("my Swag Labs cart should contain {count:d} items")
def step_swag_labs_cart_count(context, count):
    badge = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
        )
    )
    assert badge.text == str(count)


@then("my Swag Labs cart should be empty")
def step_swag_labs_cart_empty(context):
    WebDriverWait(context.behave_driver, 15).until(
        lambda driver: not driver.find_elements(
            By.CSS_SELECTOR, "[data-test='shopping-cart-badge']"
        )
    )


@then("the Swag Labs product list should be back")
def step_swag_labs_product_list_back(context):
    products = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-test='inventory-item']")
        )
    )
    assert len(products) == 6


@then('my Swag Labs cart should list "{product_name}"')
def step_swag_labs_cart_lists_product(context, product_name):
    products = context.behave_driver.find_elements(
        By.CSS_SELECTOR, "[data-test='inventory-item-name']"
    )
    product_names = [product.text for product in products]
    assert product_name in product_names


@then('the Swag Labs product "{product_name}" should offer "{button_label}"')
def step_swag_labs_product_button_label(context, product_name, button_label):
    products = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-test='inventory-item']")
        )
    )
    for product in products:
        name = product.find_element(
            By.CSS_SELECTOR, "[data-test='inventory-item-name']"
        )
        if name.text == product_name:
            assert product.find_element(By.TAG_NAME, "button").text == button_label
            return
    raise AssertionError(f"Swag Labs catalog does not contain {product_name!r}")


@then('the Swag Labs product details should show "{product_name}"')
def step_swag_labs_product_details_name(context, product_name):
    details_name = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
        )
    )
    assert details_name.text == product_name


@then('the Swag Labs product details should cost "{price}"')
def step_swag_labs_product_details_price(context, price):
    details_price = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
        )
    )
    assert details_price.text == price


@then('the first Swag Labs product should be "{product_name}"')
def step_first_swag_labs_product(context, product_name):
    first_product = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
        )
    )
    assert first_product.text == product_name


@then('the first Swag Labs product should cost "{price}"')
def step_first_swag_labs_product_price(context, price):
    first_price = context.behave_driver.find_element(
        By.CSS_SELECTOR, "[data-test='inventory-item-price']"
    )
    assert first_price.text == price


@then('the Swag Labs catalog should be headed "{heading}"')
def step_swag_labs_catalog_heading(context, heading):
    catalog_heading = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='title']"))
    )
    assert catalog_heading.text == heading


@then("the Swag Labs catalog should list {count:d} products")
def step_swag_labs_catalog_product_count(context, count):
    products = WebDriverWait(context.behave_driver, 15).until(
        EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-test='inventory-item']")
        )
    )
    assert len(products) == count


@then('the Swag Labs catalog should include "{product_name}"')
def step_swag_labs_catalog_includes_product(context, product_name):
    product_names = [
        item.text
        for item in context.behave_driver.find_elements(
            By.CSS_SELECTOR, "[data-test='inventory-item-name']"
        )
    ]
    assert product_name in product_names


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


@when('I enter "{username}" as my Swag Labs username')
def step_enter_swag_labs_username(context, username):
    context.behave_driver.find_element(
        By.CSS_SELECTOR, "[data-test='username']"
    ).send_keys(username)


@then('the Swag Labs username field should contain "{username}"')
def step_swag_labs_username_contains(context, username):
    field = context.behave_driver.find_element(
        By.CSS_SELECTOR, "[data-test='username']"
    )
    assert field.get_attribute("value") == username


@then("the Swag Labs password field should still be empty")
def step_swag_labs_password_field_still_empty(context):
    field = context.behave_driver.find_element(
        By.CSS_SELECTOR, "[data-test='password']"
    )
    assert field.get_attribute("value") == ""
