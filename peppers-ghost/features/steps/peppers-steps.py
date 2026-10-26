from behave import given, when, then
from selenium.webdriver import *
from selenium.webdriver.common.by import By

@Given("I open the instructables peppers ghost page")
def step_open_page(context):
    context.behave_driver.get("https://www.instructables.com/Peppers-Ghost-Illusion-in-a-Small-Space/")

@Then("I expect that there is at least one picture there")
def step_check_for_picture(context):
    images = context.behave_driver.find_elements(By.CSS_SELECTOR, "img") 
    assert images != []

