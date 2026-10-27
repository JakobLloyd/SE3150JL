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