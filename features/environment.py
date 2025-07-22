import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from application.app import Application
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

def browser_init(context, scenario):
    """
    Initializes the WebDriver based on the BROWSER environment variable.
    Supports local (Chrome/Firefox) and cloud (BrowserStack).
    """
    browser = os.getenv("BROWSER", "chrome").lower()
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    run_on = os.getenv("RUN_ON", "local").lower()  # "local" or "browserstack"

    if run_on == "browserstack":
        bs_user = os.getenv("BROWSERSTACK_USERNAME")
        bs_key = os.getenv("BROWSERSTACK_ACCESS_KEY")

        options = ChromeOptions()
        options.set_capability("browserName", "Chrome")
        options.set_capability("browserVersion", "114.0")
        options.set_capability("bstack:options", {
            "os": "Windows",
            "osVersion": "10",
            "userName": bs_user,
            "accessKey": bs_key,
            "buildName": "Reelly Build",
            "sessionName": scenario.name,
            "debug": True,
            "networkLogs": True
        })

        context.driver = webdriver.Remote(
            command_executor="https://hub-cloud.browserstack.com/wd/hub",
            options=options
        )


    else:
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

    print(f"RUN_ON ENV = {run_on} | BROWSER = {browser}")
    context.driver.implicitly_wait(5)
    context.app = Application(context.driver)

    context.email = os.getenv("REELLY_EMAIL")
    context.password = os.getenv("REELLY_PASSWORD")


def before_all(context):
    if os.path.exists("features/test_results/screenshots"):
        shutil.rmtree("features/test_results/screenshots")


def before_scenario(context, scenario):
    print(f'\n Started scenario: {scenario.name}')

    browser = os.getenv("BROWSER", "chrome").lower()
    print(f" Running scenario in: {browser.upper()}")

    try:
        # Init browser
        browser_init(context, scenario)
        context.driver.maximize_window()

        # Go to site
        base_url = os.getenv("BASE_URL", "https://soft.reelly.io")
        context.driver.get(base_url + "/sign-in")

        # Clear storage
        context.driver.delete_all_cookies()
        context.driver.execute_script("window.localStorage.clear();")
        context.driver.execute_script("window.sessionStorage.clear();")

    except Exception as e:
        print(f"Error starting browser for scenario '{scenario.name}': {e}")
        context.driver = None


def before_step(context, step):
    print('\n Started step: ', step.name)


def after_step(context, step):
    if step.status == "failed" and hasattr(context, "driver") and context.driver:
        screenshots_dir = os.path.join("features", "test_results", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        browser = os.getenv("BROWSER", "browser").lower()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        scenario_name = context.scenario.name.replace(" ", "_")
        step_name = step.name.replace(" ", "_")
        file_name = f"{scenario_name}_{step_name}_{browser}_{timestamp}.png"
        screenshot_path = os.path.join(screenshots_dir, file_name)

        context.driver.save_screenshot(screenshot_path)
        print(f" Screenshot saved: {screenshot_path}")


def after_scenario(context, scenario):
    if hasattr(context, "driver") and context.driver:
        context.driver.quit()
