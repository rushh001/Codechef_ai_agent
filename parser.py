from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def parse_problem(problem_link):
    """Scrapes the full problem statement from a CodeChef problem page."""
    
    driver = webdriver.Chrome()
    driver.get(problem_link)

    try:
        # Wait for the problem statement to load
        problem_statement = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'problem-statement')]"))
        )

        problem_text = problem_statement.text  # Extract text
        print(f"✅ Successfully extracted problem statement:\n{problem_text[:500]}...")  # Print first 500 chars

        return problem_text

    except Exception as e:
        print(f"❌ Error extracting problem statement: {e}")
        return None
    
    finally:
        driver.quit()  # Close browser after extraction

