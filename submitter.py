import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv

# 🌎 Load environment variables from .env file
load_dotenv()
USERNAME = os.getenv("CODECHEF_USERNAME")
PASSWORD = os.getenv("CODECHEF_PASSWORD")

def submit_solution(problem_link, solution_code):
    options = uc.ChromeOptions()
    options.headless = False  # Set to True for headless mode
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection

    driver = uc.Chrome(options=options)

    try:
        print("🔹 Opening CodeChef login page...")
        driver.get("https://www.codechef.com/login")
        time.sleep(3)  # Wait for page load

        # 🔑 Click on Login Button
        try:
            login_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Login')]")
            login_button.click()
            time.sleep(5)
        except:
            print("⚠️ No separate login button found. Skipping click.")

        # 📩 Enter Username
        print("🔹 Entering username...")
        username_input = driver.find_element(By.ID, "edit-name")
        username_input.send_keys(USERNAME)

        # 🔒 Enter Password
        print("🔹 Entering password...")
        password_input = driver.find_element(By.ID, "edit-pass")
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)  # Press Enter

        print("🔹 Waiting for login to complete...")
        time.sleep(5)  # Allow time for authentication

        # Check if CAPTCHA appears
        if "captcha" in driver.page_source.lower():
            input("⚠️ CAPTCHA detected! Solve manually and press Enter to continue...")

        # ✅ Navigate to Problem Page
        print(f"🔹 Opening problem page: {problem_link}")
        driver.get(problem_link)
        

        # 📝 Inject Solution into Ace Editor
        print("🔹 Inserting solution code...")
        time.sleep(15)
        formatted_code = solution_code.replace("\\", "\\\\").replace("`", "\\`")  # Escape special characters
        ace_script = f"""
        var editor = ace.edit("submit-ide-v2");
        editor.setValue(`{formatted_code}`);
        editor.session.selection.clearSelection();
        """
        driver.execute_script(ace_script)

        # 🚀 Click the Submit Button
        print("🔹 Submitting solution...")
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        ActionChains(driver).move_to_element(submit_button).click().perform()

        time.sleep(100)  # Wait for submission confirmation
        print("✅ Solution submitted successfully!")
        return "✅ Solution submitted successfully!"

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return f"❌ Error: {str(e)}"

