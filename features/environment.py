import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from application.app import Application
from dotenv import load_dotenv
from datetime import datetime


def browser_init(context):
    """
    :param context: Behave context
    """
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    context.driver = webdriver.Chrome(service=service)

    context.driver.maximize_window()
    context.driver.implicitly_wait(5)
    context.app = Application(context.driver)

    load_dotenv()  # load the .env file

    context.email = os.getenv("REELLY_EMAIL")
    context.password = os.getenv("REELLY_PASSWORD")


def before_scenario(context, scenario):
    print('\nStarted scenario: ', scenario.name)
    browser_init(context)


def before_step(context, step):
    print('\nStarted step: ', step)


def after_step(context, step):
    if step.status == "failed":
        # Create screenshots folder (if it doesn't exist)
        screenshots_dir = os.path.join("features", "test_results", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        # Format file name: scenario_step_timestamp.png
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        scenario_name = context.scenario.name.replace(" ", "_")
        step_name = step.name.replace(" ", "_")
        file_name = f"{scenario_name}_{step_name}_{timestamp}.png"

        # Full path
        screenshot_path = os.path.join(screenshots_dir, file_name)

        # Take the screenshot
        context.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")


    def after_scenario(context, feature):
        context.driver.quit()
