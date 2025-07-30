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
    This function opens the browser so we can run our test.
    It checks what kind of browser to use, where to run it, and if it should look like a phone.
    """

    # Get settings from your .env file
    browser = os.getenv("BROWSER", "chrome").lower()              # Chrome or Firefox?
    headless = os.getenv("HEADLESS", "false").lower() == "true"   # Hide the browser window?
    run_on = os.getenv("RUN_ON", "local").lower()                 # Run local or on BrowserStack?
    mobile = os.getenv("MOBILE_EMULATION", "false").lower() == "true"  # Run on mobile?

    # If using BrowserStack
    if run_on == "browserstack":
        bs_user = os.getenv("BROWSERSTACK_USERNAME")
        bs_key = os.getenv("BROWSERSTACK_ACCESS_KEY")

        # Set up BrowserStack Chrome settings
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

        # Start browser in the cloud
        context.driver = webdriver.Remote(
            command_executor="https://hub-cloud.browserstack.com/wd/hub",
            options=options
        )

    # If running local
    else:
        if browser == "chrome":
            options = ChromeOptions()

            # If mobile
            if mobile:
                # Select mobile device
                mobile_emulation = {"deviceName": os.getenv("DEVICE_NAME", "Nexus 5")}
                options.add_experimental_option("mobileEmulation", mobile_emulation)

                # Add special settings so headless Chrome runs better
                options.add_argument("--headless=new")            # Don't show browser window
                options.add_argument("--disable-gpu")             # GPU causes issues sometimes
                options.add_argument("--no-sandbox")              # Helps it run in some systems
                options.add_argument("--disable-dev-shm-usage")   # Fix memory issues in some environments

                # Start browser using Selenium Server at localhost
                context.driver = webdriver.Remote(
                    command_executor='http://127.0.0.1:4444/wd/hub',
                    options=options
                )

            # If NOT using mobile mode
            else:
                if headless:
                    options.add_argument("--headless=new")
                    options.add_argument("--window-size=1920,1080")
                    options.add_argument("--disable-gpu")
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")

                # Get the ChromeDriver (installs automatically)
                service = ChromeService(ChromeDriverManager().install())

                # Start local Chrome browser
                context.driver = webdriver.Chrome(service=service, options=options)

        elif browser == "firefox":
            options = FirefoxOptions()

            if headless:
                options.add_argument("--headless")

            service = FirefoxService(GeckoDriverManager().install())
            context.driver = webdriver.Firefox(service=service, options=options)

        else:
            raise Exception(f"Unsupported browser: {browser}")


    print(f"RUN_ON ENV = {run_on} | BROWSER = {browser} | MOBILE_EMULATION = {mobile}")

    # Set how long to wait for things to appear before failing
    context.driver.implicitly_wait(5)

    # Create the app object
    context.app = Application(context.driver)

    # Get login info from the .env file
    context.email = os.getenv("REELLY_EMAIL")
    context.password = os.getenv("REELLY_PASSWORD")


def before_all(context):
    if os.path.exists("features/test_results/screenshots"):
        shutil.rmtree("features/test_results/screenshots")


def before_scenario(context, scenario):
    # Print the name of the scenario being started
    print(f'\n Started scenario: {scenario.name}')

    # Read environment variables for browser and mobile emulation mode
    browser = os.getenv("BROWSER", "chrome").lower()
    mobile = os.getenv("MOBILE_EMULATION", "false").lower() == "true"

    try:
        # Initialize the browser based on env settings (local/cloud/mobile/etc.)
        browser_init(context, scenario)

        # Maximize the browser window only if not running in mobile emulation mode
        # (Mobile emulation does not support window manipulation)
        if not mobile:
            context.driver.maximize_window()

        # Navigate to the Reelly sign-in page
        base_url = os.getenv("BASE_URL", "https://soft.reelly.io")
        context.driver.get(base_url + "/sign-in")

        # Clear cookies and browser storage to ensure a clean test session
        # NOTE: This is optional for mobile, but kept here unless device issues arise
        if not mobile:
            context.driver.delete_all_cookies()
            context.driver.execute_script("window.localStorage.clear();")
            context.driver.execute_script("window.sessionStorage.clear();")

    except Exception as e:
        # Log any startup error and ensure driver is set to None to prevent further failures
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
