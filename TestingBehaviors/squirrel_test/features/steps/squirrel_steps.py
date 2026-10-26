import time
from behave import given, when, then
from selenium.webdriver.common.by import By

URL = "http://localhost:8000"

def get_rows(context):
    return context.behave_driver.find_elements(By.CSS_SELECTOR, "#squirrels-list li")


def get_names(context):
    names = context.behave_driver.find_elements(By.CSS_SELECTOR, "#squirrels-list li .name")
    return [n.text for n in names]

@given("I open Squirreltown")
def step_open(context):
    context.behave_driver.get(URL)