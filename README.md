## Careerist Test Automation Repository
Automated UI testing for https://www.careerist.com/automation

Built with **Python 3** and **Behave (BDD)** using **Selenium WebDriver**.


---

##  What This Framework Does

- Runs UI tests using the Page Object Model (POM)
- Supports mobile emulation (yep, test like you're on a phone!)
- Works locally or with BrowserStack for cloud-based testing
- Uses Gherkin-style test cases for readable, behavior-driven testing
- Captures screenshots automatically on failures
- Auto-cleans sessions and browser state between tests

---

## Setup: Environment Variables

To get started, copy and configure your `.env`:

```bash
cp .env.example .env

BASE_URL=https://soft.reelly.io
REELLY_EMAIL=your_email@example.com
REELLY_PASSWORD=your_password
HEADLESS=false  # or true
BROWSER=chrome  # or firefox
RUN_ON=local    # or browserstack
DEVICE_NAME=Nexus 5  # Optional for mobile emulation
BROWSERSTACK_USERNAME=your_browserstack_username
BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key

#If DEVICE_NAME isn't set, it defaults to "Nexus 5"
```
---

## Cross-Browser & Cloud Testing
This project supports:
- Chrome and Firefox (via WebDriverManager)
- BrowserStack for cloud testing 

The framework will automatically:
- Launch your selected browser 
- Maximize the window (desktop mode)
- Handle mobile emulation (if configured)
- Clear cookies and local storage before each scenario 
- Take screenshots on any step failure
---

## Architecture: POM + Behave
- Page Object Model (POM) is used to keep your page interactions clean and DRY. 
- Business logic is abstracted into page classes like MainPage, SecondaryPage, etc. 
- Tests are written in Gherkin for human-readable scenarios.
---

## Screenshots & Test Results
Failed steps will auto-save screenshots to:
```
features/test_results/screenshots/
```
Filenames include:
- Scenario name 
- Step name 
- Browser used 
- Timestamp
---

## Requirements
- Python 3.10+ 
- Chrome and/or Firefox installed 
- Java installed (for Selenium Grid / Standalone server if used)
```
pip install -r requirements.txt
```
---

## Future Development
- Refactor environment.py into modular helper files for easier maintenance 
- Add support for parallel test execution 
- Improve test coverage across all listing filters 
- Add CI/CD integration (e.g. GitHub Actions or Jenkins)
- Expand mobile emulation testing with additional devices 
- Add HTML or Allure test reporting

## Contributing / Support
This repo was built as part of the Careerist Automation Program.
Feel free to fork it, play with it, or message with questions if you're diving into QA automation!

--- 