from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.helpers import is_mobile_mode
from time import sleep


class SecondaryPage(BasePage):
    ##DESKTOP LOCATORS
    SECONDARY_BTN = (By.XPATH, "//div[text()='Secondary']")
    FILTERS_BTN = (By.CSS_SELECTOR, '.filter-text')
    UNIT_PRICE_LABELS = (By.CSS_SELECTOR, '.number-price-text')
    secondary_page_partial_url = 'secondary-listings'

    ##MOBILE LOCATORS
    OFF_PLAN_BTN = (By.CSS_SELECTOR, "a[wized='newOffPlanLink'][href='https://find.reelly.io/']")
    MOBILE_SECONDARY_BTN = (By.XPATH, "//button[text()='Secondary']")
    MOBILE_FILTERS_BTN = (By.CSS_SELECTOR, "[wized='openFiltersWindow']")


    def select_secondary_option(self):
        if is_mobile_mode(self.driver):
            self.wait_for_element_click(*self.OFF_PLAN_BTN)
            self.wait_for_element_click(*self.MOBILE_SECONDARY_BTN)
        else:
            self.wait_for_element_click(*self.SECONDARY_BTN)


    def verify_secondary_page_opened(self):
        self.verify_partial_url(self.secondary_page_partial_url)


    def select_filters_button(self):
        sleep(5)
        if is_mobile_mode(self.driver):
            self.wait_for_element_click(*self.MOBILE_FILTERS_BTN)
        else:
            self.click(*self.FILTERS_BTN)


    def get_displayed_unit_prices(self):
        price_elements = self.find_elements(*self.UNIT_PRICE_LABELS)
        print(f"Raw price elements found: {len(price_elements)}")

        prices = []
        for el in price_elements:
            if not el.is_displayed():
                continue  # Skip hidden ones

            text = el.text.replace("AED", "").replace(",", "").strip()
            if text and text.isdigit():
                prices.append(int(text))

        print(f"Visible price elements processed: {len(prices)}")
        return prices or []


    def verify_prices_in_range(self, min_price, max_price):
        prices = self.get_displayed_unit_prices()
        if not prices:
            raise AssertionError(
                "No visible or valid price elements found. Filter may not have applied or the page didn't render correctly.")

        for price in prices:
            assert min_price <= price <= max_price, f"Price {price} is out of range ({min_price}-{max_price})"

        print(f"All {len(prices)} prices are within range: {min_price}-{max_price}")





