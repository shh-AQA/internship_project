import os
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from time import sleep


class MainPage(BasePage):
    EMAIL_INPUT = (By.ID, 'email-2')
    PASSWORD_INPUT = (By.ID, 'field')
    CONTINUE_BTN = (By.CSS_SELECTOR, '.login-button.w-button')
    SIGN_IN_PATH = "/sign-in"


    def open_main_page(self):
        base_url = os.getenv("BASE_URL", "https://soft.reelly.io")
        full_url = f"{base_url}{self.SIGN_IN_PATH}"
        print(f"Navigating to: {full_url}")
        self.driver.get(full_url)

    def login(self, email, password):
        self.wait_for_element(*self.EMAIL_INPUT)
        self.input_text(email, *self.EMAIL_INPUT)

        self.wait_for_element(*self.PASSWORD_INPUT)
        self.input_text(password, *self.PASSWORD_INPUT)

        self.wait_for_element_click(*self.CONTINUE_BTN)




