from selenium.webdriver.common.by import By
from behave import given, when, then

@given('the user opens the Reelly main page')
def open_main_page(context):
    context.app.main_page.open_main_page()


@given('the user logs into the page')
def user_login(context):
    context.app.main_page.login(context.email, context.password)

