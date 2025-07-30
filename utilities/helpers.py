import os

def is_mobile_mode(driver=None):
    """
    Detects if the current run is in mobile emulation mode.
    Uses .env flag and optionally checks browser user agent.
    """
    env_flag = os.getenv("MOBILE_EMULATION", "false").lower() == "true"

    if driver:
        try:
            user_agent = driver.execute_script("return navigator.userAgent;")
            return env_flag or "Mobile" in user_agent
        except Exception:
            return env_flag

    return env_flag
