from selenium.webdriver.common.by import By
from behave import given, when, then

@when('sets the price range from {min_price:d} to {max_price:d} AED')
def step_set_price_range(context, min_price, max_price):
    context.min_price = min_price
    context.max_price = max_price

    context.app.filters_overlay.set_price_filter(min_price, max_price)
