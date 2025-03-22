import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Set UTF-8 Encoding
sys.stdout.reconfigure(encoding='utf-8')

# File to track the last fetched problem
COUNTER_FILE = "counter.txt"
MAX_INDEX = 400  # Reset after 400

# Function to read the counter value
def load_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0
    return 0  # Default if file doesn't exist

# Function to save the counter value
def save_counter(counter):
    with open(COUNTER_FILE, "w") as file:
        file.write(str(counter))

# Load last saved counter
problem_counter = load_counter()

def get_daily_easy_problem():
    global problem_counter

    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model (useful for servers)
    options.add_argument("--disable-dev-shm-usage")  # Prevents Chrome crashes in Docker/Linux
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")  # Spoof User-Agent

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.codechef.com/practice/basic-programming-concepts")

        retries = 3  # Number of retries if timeout occurs
        for attempt in range(retries):
            try:
                problems = WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, '_tableBody_')]//a[contains(@class, '_problemName_')]"))
                )
                break  # Exit loop if successful
            except Exception as e:
                print(f"Attempt {attempt+1}: Retrying due to timeout...")
                time.sleep(5)  # Wait before retrying
        else:
            raise TimeoutError("Failed to load problems after multiple attempts.")

        if problem_counter >= len(problems):
            print(f"Index {problem_counter} is out of range. Resetting to 0.")
            problem_counter = 0  # Reset if it goes beyond available problems

        # Extract problem details
        problem_name = problems[problem_counter].text
        problem_link = problems[problem_counter].get_attribute("href")

        print(f"Extracted Problem Name: {problem_name}")
        print(f"Extracted Problem Link: {problem_link}")

        # Increment counter (reset if it reaches MAX_INDEX)
        problem_counter = (problem_counter + 1) % (MAX_INDEX + 1)
        save_counter(problem_counter)

        print(f"Counter Updated: {problem_counter}")

        return problem_name, problem_link

    except Exception as e:
        print(f"Error in scraping: {e}")
        return None, None  

    finally:
        driver.quit()  # Ensure ChromeDriver quits properly

# Test the function
# get_daily_easy_problem()
