import behave_webdriver
from selenium.webdriver.chrome.options import Options

def before_all(context):
    options = Options()
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    context.behave_driver = behave_webdriver.Chrome()


def after_all(context):
    context.behave_driver.quit()
