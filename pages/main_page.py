from selenium.webdriver.common.by import By
from pages.base_page import BasePage



class MainPage(BasePage):
    EMAIL_INPUT = (By.ID, 'email-2')
    PASSWORD_INPUT = (By.ID, 'field')
    CONTINUE_BTN = (By.CSS_SELECTOR, '.login-button.w-button')

    def open_main_page(self):
        self.driver.get('https://soft.reelly.io')


    def login(self, email, password):
            self.input_text(email, *self.EMAIL_INPUT)
            self.input_text(password, *self.PASSWORD_INPUT)
            self.click(*self.CONTINUE_BTN)
