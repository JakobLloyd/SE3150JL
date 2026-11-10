import os

import behave_webdriver
from selenium.webdriver.chrome.options import Options

def before_all(context):
    options = Options()
    if os.environ.get("CI"):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    context.behave_driver = behave_webdriver.Chrome(options=options)


def after_all(context):
    context.behave_driver.quit()
