import os
import subprocess

for browser in ["chrome", "firefox"]:
    print(f"\n🚀 Running tests in {browser.upper()}")
    os.environ["BROWSER"] = browser
    subprocess.run(["behave"])
