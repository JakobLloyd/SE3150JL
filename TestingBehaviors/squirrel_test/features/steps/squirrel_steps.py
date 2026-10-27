from behave import given, when, then
from selenium.webdriver import *
from selenium.webdriver.common.by import By

URL = "http://localhost:8000"

@Given("I open Squirreltown")
def step_open(context):
    context.behave_driver.get("http://localhost:8000")

@Then('the page title is "{title}"')
def step_title(context, title):
    assert context.behave_driver.title == title

@Then('the heading says "{text}"')
def step_heading(context, text):
    heading = context.behave_driver.find_element(By.TAG_NAME, "h1")
    assert heading.text == text

@Then("the dialog is hidden")
def step_dialog_hidden(context):
    dialog = context.behave_driver.find_element(By.ID, "squirrel-dialog")
    assert dialog.is_displayed() == False

@When("I click the add button")
def step_click_add(context):
    context.behave_driver.find_element(By.ID, "add-button").click()

@Then("the dialog is visible")
def step_dialog_visible(context):
    dialog = context.behave_driver.find_element(By.ID, "squirrel-dialog")
    assert dialog.is_displayed() == True

@Then('the dialog title is "{text}"')
def step_dialog_title(context, text):
    title = context.behave_driver.find_element(By.ID, "dialog-title")
    assert title.text == text

@When("I click the cancel button")
def step_click_cancel(context):
    context.behave_driver.find_element(By.ID, "cancel-button").click()

def get_rows(context):
    return context.behave_driver.find_elements(By.CSS_SELECTOR, "#squirrels-list li")


def get_names(context):
    names = context.behave_driver.find_elements(By.CSS_SELECTOR, "#squirrels-list li .name")
    return [n.text for n in names]


@when('I add a squirrel named "{name}" with size "{size}"')
def step_add_squirrel(context, name, size):
    driver = context.behave_driver
    driver.find_element(By.ID, "add-button").click()
    driver.find_element(By.ID, "squirrel-name-input").send_keys(name)
    driver.find_element(By.ID, "squirrel-size-input").send_keys(size)
    driver.find_element(By.ID, "save-button").click()
    time.sleep(1)


@when("I click the delete button on the last squirrel")
def step_click_delete(context):
    get_rows(context)[-1].find_element(By.CSS_SELECTOR, ".fa-trash").click()


@when("I accept the popup")
def step_accept_popup(context):
    context.behave_driver.switch_to.alert.accept()
    time.sleep(1)


@then('the popup says "{text}"')
def step_popup_says(context, text):
    assert text in context.behave_driver.switch_to.alert.text


@then('the squirrel list contains "{name}"')
def step_list_contains(context, name):
    for _ in range(30):
        if name in get_names(context):
            return
        time.sleep(0.5)
    assert False, f"{name} was not in the list"


@then('the squirrel list does not contain "{name}"')
def step_list_missing(context, name):
    for _ in range(30):
        if name not in get_names(context):
            return
        time.sleep(0.5)
    assert False, f"{name} was still in the list"