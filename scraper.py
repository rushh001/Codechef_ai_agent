from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_daily_easy_problem():
    driver = webdriver.Chrome()
    driver.get("https://www.codechef.com/practice/basic-programming-concepts")

    try:
        # Wait for the first problem link
        first_problem = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, '_tableBody_')]//a[contains(@class, '_problemName_')]"))
        )

        problem_name = first_problem[6].text
        problem_link = first_problem[6].get_attribute("href")

        # Debugging output
        print(f"🔹 Extracted Problem Name: {problem_name}")
        print(f"🔹 Extracted Problem Link: {problem_link}")

        if not problem_link:
            print("❌ Error: Problem link extraction failed.")
        print(f"🔹 Problem Link Extracted: {problem_link}")  # Debugging
        return problem_name, problem_link

    except Exception as e:
        print(f"❌ Error in scraping: {e}")
        return None, None  

    

# Test the function
get_daily_easy_problem()