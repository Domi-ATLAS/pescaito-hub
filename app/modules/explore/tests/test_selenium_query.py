import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def wait_for_page_to_load(driver, timeout=1000):
    """Waits for the page to fully load."""
    WebDriverWait(driver, timeout).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )


def test_search_functionality():
    """Tests the search functionality on the explore page."""
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()

        # Log in
        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")
        password_field.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        # Navigate to the Explore page
        driver.get(f"{host}/explore")
        wait_for_page_to_load(driver)

        # Input search parameters
        query_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "query"))
        )
        query_field.clear()
        query_field.send_keys('title:"Sample dataset 2"')

        # Submit the search form
        wait_for_page_to_load(driver)

        # Validate the results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "results"))
        )
        results_container = driver.find_element(By.ID, "results")
        results = results_container.find_elements(By.CLASS_NAME, "card")
        
        assert len(results) > 0, "No search results found!"

        # Output results for debugging
        for result in results:
            title = result.find_element(By.TAG_NAME, "h3").text
            print(f"Found dataset: {title}")

        print("Search functionality test passed!")

    except Exception as e:
        print(f"Test failed due to error: {e}")
    finally:
        # Close the browser
        close_driver(driver)


# Run the test
if __name__ == "__main__":
    test_search_functionality()
