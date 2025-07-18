from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from time import sleep

class FiltersOverlay(BasePage):
    MIN_UNIT_PRICE = (By.CSS_SELECTOR, "[wized='unitPriceFromFilter']")
    MAX_UNIT_PRICE = (By.CSS_SELECTOR, "[wized='unitPriceToFilter']")
    APPLY_FILTER_BTN = (By.CSS_SELECTOR, "[wized='applyFilterButtonMLS']")


    def set_price_filter(self, price_from, price_to):
        self.find_element(*self.MIN_UNIT_PRICE).send_keys(price_from)
        self.find_element(*self.MAX_UNIT_PRICE).send_keys(price_to)
        self.click(*self.APPLY_FILTER_BTN)
        sleep(5)