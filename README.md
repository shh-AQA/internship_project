## Careerist Test Automation Repository
Automated UI testing for https://www.careerist.com/automation

Built with **Python 3** and **Behave (BDD)** using **Selenium WebDriver**.

## 🔐 Credentials & Environment Variables
To configure login credentials and settings:

1. Copy the example file:

        cp .env.example .env


2. Fill in your values:


    BASE_URL=https://soft.reelly.io
    REELLY_EMAIL=your_email@example.com
    REELLY_PASSWORD=your_password
    HEADLESS=false
    BROWSER=chrome


## 🌐Cross-Browser Testing
This project supports both Chrome and Firefox via Selenium and WebDriverManager.

Built-in environment hooks will:

    Launch your selected browser
    Maximize window
    Clear session/cookies
    Handle screenshots on failure


## 📸 Test Reports & Screenshots
On failure, screenshots are automatically saved to:

    features/test_results/screenshots/

Filenames include the scenario, step, browser, and timestamp.


## 🧱 Architecture
This framework follows the Page Object Model (POM) for maintainability and reuse.
Each page interaction lives in a class (e.g., MainPage, SecondaryPage) to separate logic from tests.

Behave is used for its Gherkin syntax, which supports BDD-style readable test cases.

## 🔧 Requirements
Python 3.10+

Chrome & Firefox browsers installed

Install dependencies:
        
        pip install -r requirements.txt


## 🙋‍♀️ Support
This repo was built during the Careerist Automation program.
If you're using it for your own learning or projects, feel free to fork or reach out with questions.
