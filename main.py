import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import traceback

def click_sign_icon(driver, ns_random):
    """
    尝试点击签到图标和试试手气按钮的通用方法
    """
    try:
        print("开始查找签到图标...")
        # 使用更精确的选择器定位签到图标
        # IMPORTANT: Replace this XPath with the precise XPath for your forum's sign-in icon
        sign_icon_xpath = os.environ.get('SIGN_ICON_XPATH', "//span[@title='签到']")

        sign_icon = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, sign_icon_xpath))
        )
        print("找到签到图标，准备点击...")

        # 确保元素可见和可点击
        driver.execute_script("arguments[0].scrollIntoView(true);", sign_icon)
        time.sleep(0.5)

        # 打印元素信息
        print(f"签到图标元素: {sign_icon.get_attribute('outerHTML')}")

        # 尝试点击
        try:
            sign_icon.click()
            print("签到图标点击成功")
        except Exception as click_error:
            print(f"点击失败，尝试使用 JavaScript 点击: {str(click_error)}")
            driver.execute_script("arguments[0].click();", sign_icon)

        print("等待页面跳转...")
        time.sleep(5) # Adjust based on your forum's load time

        # 打印当前URL
        print(f"当前页面URL: {driver.current_url}")

        # 点击"试试手气"按钮
        try:
            click_button = None

            # IMPORTANT: Replace these XPaths with the precise XPaths for your forum's buttons
            if ns_random:
                lucky_button_xpath = os.environ.get('LUCKY_BUTTON_XPATH', "//button[contains(text(), '试试手气')]")
                click_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, lucky_button_xpath))
                )
            else:
                chicken_button_xpath = os.environ.get('CHICKEN_BUTTON_XPATH', "//button[contains(text(), '鸡腿 x 5')]")
                click_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, chicken_button_xpath))
                )

            click_button.click()
            print("完成试试手气点击")
        except Exception as lucky_error:
            print(f"试试手气按钮点击失败或者签到过了: {str(lucky_error)}")

        return True

    except Exception as e:
        print(f"签到过程中出错:")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"当前页面URL: {driver.current_url}")
        print(f"当前页面源码片段: {driver.page_source[:500]}...")
        print("详细错误信息:")
        traceback.print_exc()
        return False

def main():
    # --- Configuration ---
    FORUM_URL = os.environ.get('FORUM_URL', 'YOUR_FORUM_LOGIN_URL') # IMPORTANT: Replace with your forum's login URL
    USERNAME = os.environ.get('FORUM_USERNAME', 'YOUR_USERNAME')
    PASSWORD = os.environ.get('FORUM_PASSWORD', 'YOUR_PASSWORD')
    FORUM_COOKIES = os.environ.get('FORUM_COOKIES', '') # Optional: JSON string of cookies for login
    # IMPORTANT: Replace these XPaths/Selectors with the precise ones for your forum
    USERNAME_SELECTOR = os.environ.get('USERNAME_SELECTOR', 'input[name="username"]')
    PASSWORD_SELECTOR = os.environ.get('PASSWORD_SELECTOR', 'input[name="password"]')
    LOGIN_BUTTON_SELECTOR = os.environ.get('LOGIN_BUTTON_SELECTOR', 'button[type="submit"]')
    NS_RANDOM = os.environ.get('NS_RANDOM', 'True').lower() == 'true' # For "试试手气" or "鸡腿 x 5"

    print("Starting undetected_chromedriver...")
    driver = uc.Chrome(headless=True, use_subprocess=True) # Set headless=True for GitHub Actions
    # driver.maximize_window() # Optional: maximize window if needed for element visibility

    logged_in_with_cookies = False

    try:
        if FORUM_COOKIES:
            print("Attempting to log in with cookies...")
            try:
                # Navigate to the domain first to set cookies
                driver.get(FORUM_URL) # This is crucial for cookies to be set for the correct domain
                cookies = json.loads(FORUM_COOKIES)
                for cookie in cookies:
                    # Remove 'domain' and 'expires' if they cause issues, or ensure they match
                    # Some sites require 'domain' to be exact, others are fine without it
                    if 'domain' in cookie:
                        del cookie['domain']
                    if 'expires' in cookie: # Convert float to int if present and not already
                        cookie['expires'] = int(cookie['expires']) if isinstance(cookie['expires'], float) else cookie['expires']

                    # Ensure essential fields are present
                    if 'name' in cookie and 'value' in cookie:
                        driver.add_cookie(cookie)
                driver.get(FORUM_URL) # Reload page with cookies
                print("Cookies set successfully. Checking if logged in...")
                # You might want to add a check here to see if the user is actually logged in
                # e.g., look for a 'welcome user' text or absence of login form
                # For simplicity, we'll assume setting cookies is enough to bypass login page
                logged_in_with_cookies = True
                print("Logged in with cookies.")
            except Exception as cookie_error:
                print(f"Failed to log in with cookies: {cookie_error}. Falling back to username/password login.")
                traceback.print_exc()

        if not logged_in_with_cookies:
            print(f"Navigating to {FORUM_URL}")
            driver.get(FORUM_URL)

            # --- Login Process (if not logged in with cookies) ---
            print('Attempting to log in with username/password...')
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, USERNAME_SELECTOR))
            ).send_keys(USERNAME)
            driver.find_element(By.CSS_SELECTOR, PASSWORD_SELECTOR).send_keys(PASSWORD)

            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_BUTTON_SELECTOR))
            ).click()

            print('Login attempt complete.')

        print(f"Current URL after initial login/cookie setup: {driver.current_url}")

        # --- Sign-in Process ---
        click_sign_icon(driver, NS_RANDOM)

        print('Automation script finished successfully.')

    except Exception as e:
        print('Automation script failed:', e)
        traceback.print_exc()
        driver.quit()
        exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
