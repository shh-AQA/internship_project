from selenium.webdriver.common.by import By
from behave import given, when, then

@when('the user clicks on the "Secondary" option in the left menu')
def select_secondary_option(context):
    context.app.secondary_page.select_secondary_option()

@when('the user clicks on the Filters button')
def select_filters_button(context):
    context.app.secondary_page.select_filters_button()

@then('the Secondary page should open')
def verify_secondary_page(context):
    context.app.secondary_page.verify_secondary_page_opened()

@then('all displayed cards should have prices within that range')
def verify_prices_in_range(context):
    context.app.secondary_page.verify_prices_in_range(
        context.min_price,
        context.max_price
    )
