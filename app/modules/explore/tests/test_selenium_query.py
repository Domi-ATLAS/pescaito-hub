import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestExplorePage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/explore")  # Afrom selenium.webdriver.support.ui import Selectjusta la URL según sea necesario
        self.wait = WebDriverWait(self.driver, 10)


    def tearDown(self):
        self.driver.quit()

    def clear_filters(self):
        clear_button = self.driver.find_element(By.ID, 'clear-filters')
        self.driver.execute_script("arguments[0].scrollIntoView();", clear_button)
        self.wait.until(EC.element_to_be_clickable((By.ID, 'clear-filters')))
        self.driver.execute_script("arguments[0].click();", clear_button)
        time.sleep(1)  # Allow time for the page to reset

    def test_query_by_title_or_author_finds(self):
        # Verifica que la funcionalidad de búsqueda funciona correctamente
        query_input = self.driver.find_element(By.ID, 'query')
        query_input.send_keys('title:"Sample dataset 3" || author:"Author 2"')
        query_input.send_keys(Keys.RETURN)
        time.sleep(2)

        results = self.driver.find_element(By.ID, 'results')
        self.assertGreater(len(results.find_elements(By.CLASS_NAME, 'card')), 0, "No se encontraron resultados")
        self.clear_filters()
        print("Encontrar por titulo o autor: OK")
                

    def test_query_by_title_and_author_finds(self):
        # Verifica que la funcionalidad de búsqueda funciona correctamente
        query_input = self.driver.find_element(By.ID, 'query')
        query_input.send_keys('title:"Sample dataset 2" && author:"Author 2"')
        query_input.send_keys(Keys.RETURN)
        time.sleep(2)

        results = self.driver.find_element(By.ID, 'results')
        self.assertGreater(len(results.find_elements(By.CLASS_NAME, 'card')), 0, "No se encontraron resultados")
        self.clear_filters()
        print("Encontrar por titulo y autor: OK")


    def test_query_by_author_finds(self):
        pass

    def test_query_by_title_no_finds(self):
        pass

    def test_query_by_description_no_finds(self):
        pass

    def test_query_by_description_no_finds(self):
        pass

    def test_mixed_query_finds(self):
        pass

    def test_mixed_query_no_finds(self):
        pass

if __name__ == "__main__":
    unittest.main()