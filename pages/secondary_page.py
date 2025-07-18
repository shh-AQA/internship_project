from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class SecondaryPage(BasePage):
    SECONDARY_BTN = (By.XPATH, "//div[text()='Secondary']")
    FILTERS_BTN = (By.CSS_SELECTOR, '.filter-text')
    UNIT_PRICE_LABELS = (By.CSS_SELECTOR, '.number-price-text')
    secondary_page_partial_url = 'secondary-listings'

    def select_secondary_option(self):
        self.wait_for_element_click(*self.SECONDARY_BTN)


    def verify_secondary_page_opened(self):
        self.verify_partial_url(self.secondary_page_partial_url)


    def select_filters_button(self):
        sleep(5)
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





