import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from application.app import Application
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()



def browser_init(context):
    """
    Initializes the WebDriver based on the BROWSER environment variable
    """
    # load_dotenv()

    browser = os.getenv("BROWSER", "chrome").lower()
    headless = os.getenv("HEADLESS", "false").lower() == "true"

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        driver_path = ChromeDriverManager().install()
        service = ChromeService(driver_path)
        context.driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")

        driver_path = GeckoDriverManager().install()
        service = FirefoxService(driver_path)
        context.driver = webdriver.Firefox(service=service, options=options)

    else:
        raise Exception(f"Unsupported browser: {browser}")

    print(f"📣 BROWSER ENV = {browser}")

    context.driver.implicitly_wait(5)
    context.app = Application(context.driver)

    context.email = os.getenv("REELLY_EMAIL")
    context.password = os.getenv("REELLY_PASSWORD")

def before_all(context):
    if os.path.exists("features/test_results/screenshots"):
        shutil.rmtree("features/test_results/screenshots")

def before_scenario(context, scenario):
    print(f'\n🧪 Started scenario: {scenario.name}')

    browser = os.getenv("BROWSER", "chrome").lower()
    print(f"🌐 Running scenario in: {browser.upper()}")

    # 1. Init browser
    browser_init(context)

    # 2. Maximize
    context.driver.maximize_window()

    # ✅ 3. Navigate to a real URL (before interacting with storage)
    base_url = os.getenv("BASE_URL", "https://soft.reelly.io")
    context.driver.get(base_url + "/sign-in")

    # ✅ 4. Now it's safe to clear
    context.driver.delete_all_cookies()
    context.driver.execute_script("window.localStorage.clear();")
    context.driver.execute_script("window.sessionStorage.clear();")


# def before_scenario(context, scenario):
#     print(f'\n🧪 Started scenario: {scenario.name}')
#
#     browser = os.getenv("BROWSER", "chrome").lower()
#     print(f"🌐 Running scenario in: {browser.upper()}")
#
#     # Initialize driver
#     browser_init(context)
#
#     #maximize window
#     context.driver.maximize_window()
#
#     # Clear cookies, localStorage, and sessionStorage before login
#     context.driver.delete_all_cookies()
#     context.driver.execute_script("window.localStorage.clear();")
#     context.driver.execute_script("window.sessionStorage.clear();")


def before_step(context, step):
    print('\n➡️ Started step: ', step.name)


def after_step(context, step):
    if step.status == "failed":
        screenshots_dir = os.path.join("features", "test_results", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        browser = os.getenv("BROWSER", "browser").lower()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        scenario_name = context.scenario.name.replace(" ", "_")
        step_name = step.name.replace(" ", "_")
        file_name = f"{scenario_name}_{step_name}_{browser}_{timestamp}.png"
        screenshot_path = os.path.join(screenshots_dir, file_name)

        context.driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")


def after_scenario(context, scenario):
    context.driver.quit()

    # If more browsers are left to test, re-run via subprocess or run_all_browsers.py
    # DO NOT re-run the scenario manually here — Behave doesn't support that




