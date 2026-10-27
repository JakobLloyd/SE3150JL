import time
from behave import given, when, then
from selenium.webdriver import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@Given("I open Squirreltown")
def step_open(context):
    context.behave_driver.get("http://localhost:8000")
    time.sleep(1)

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

@When('I add a squirrel named "{name}" with size "{size}"')
def step_add_squirrel(context, name, size):
    context.behave_driver.find_element(By.ID, "add-button").click()
    context.behave_driver.find_element(By.ID, "squirrel-name-input").send_keys(name)
    context.behave_driver.find_element(By.ID, "squirrel-size-input").send_keys(size)
    context.behave_driver.find_element(By.ID, "save-button").click()
    WebDriverWait(context.behave_driver, 15).until(EC.presence_of_element_located((By.XPATH, f"//li[div='{name}']")))
    time.sleep(1)

@When("I click the delete button on the last squirrel")
def step_delete_last(context):
    rows = context.behave_driver.find_elements(By.CSS_SELECTOR, "#squirrels-list li")
    rows[-1].find_element(By.CSS_SELECTOR, ".fa-trash").click()

@When("I accept the popup")
def step_accept_popup(context):
    context.behave_driver.switch_to.alert.accept()

@Then('the popup says "{text}"')
def step_popup_says(context, text):
    assert text in context.behave_driver.switch_to.alert.text

@Then('the squirrel list contains "{name}"')
def step_list_has(context, name):
    WebDriverWait(context.behave_driver, 15).until(EC.presence_of_element_located((By.XPATH, f"//li[div='{name}']")))

@Then('the squirrel list does not contain "{name}"')
def step_list_missing(context, name):
    WebDriverWait(context.behave_driver, 15).until_not(EC.presence_of_element_located((By.XPATH, f"//li[div='{name}']")))

@When("I dismiss the popup")
def step_dismiss_popup(context):
    context.behave_driver.switch_to.alert.dismiss()

@Then('the last squirrel has size "{size}"')
def step_last_size(context, size):
    rows = context.behave_driver.find_elements(By.CSS_SELECTOR, "#squirrels-list li")
    assert rows[-1].find_element(By.CSS_SELECTOR, ".size").text == size

@When("I click the edit button on the last squirrel")
def step_edit_last(context):
    rows = context.behave_driver.find_elements(By.CSS_SELECTOR, "#squirrels-list li")
    rows[-1].find_element(By.CSS_SELECTOR, ".fa-pencil").click()

@Then('the name box contains "{text}"')
def step_name_box(context, text):
    box = context.behave_driver.find_element(By.ID, "squirrel-name-input")
    assert box.get_attribute("value") == text

@Then('the size box contains "{text}"')
def step_size_box(context, text):
    box = context.behave_driver.find_element(By.ID, "squirrel-size-input")
    assert box.get_attribute("value") == text

@When('I change the name to "{name}"')
def step_change_name(context, name):
    box = context.behave_driver.find_element(By.ID, "squirrel-name-input")
    box.clear()
    box.send_keys(name)

@When("I click the save button")
def step_click_save(context):
    context.behave_driver.find_element(By.ID, "save-button").click()
    time.sleep(1)
