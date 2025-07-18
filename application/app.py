from pages.base_page import BasePage
from pages.filters_overlay import FiltersOverlay
from pages.main_page import MainPage
from pages.secondary_page import SecondaryPage



class Application:
    def __init__(self, driver):
        self.driver = driver
        self.base_page = BasePage(self.driver)
        self.filters_overlay = FiltersOverlay(self.driver)
        self.main_page = MainPage(self.driver)
        self.secondary_page = SecondaryPage(self.driver)