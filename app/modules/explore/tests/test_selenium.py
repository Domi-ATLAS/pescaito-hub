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

    def test_page_load(self):
        # Verifica que la página se carga correctamente
        self.assertIn("UVLHUB.IO(dev) - Repository of feature models in UVL", self.driver.title)
        print("Carga de página: OK")

    def test_search_functionality(self):
        # Verifica que la funcionalidad de búsqueda funciona correctamente
        query_input = self.driver.find_element(By.ID, 'query')
        query_input.send_keys("example search")
        query_input.send_keys(Keys.RETURN)
        time.sleep(2)

        results = self.driver.find_element(By.ID, 'results')
        self.assertGreater(len(results.find_elements(By.CLASS_NAME, 'card')), 0, "No se encontraron resultados")
        print("Funcionalidad de búsqueda: OK")

    # def test_filter_by_publication_type(self):
    #     publication_type_filter = self.driver.find_element(By.ID, 'publication_type')
    #     self.driver.execute_script("arguments[0].scrollIntoView();", publication_type_filter)
    #     self.wait.until(EC.element_to_be_clickable((By.ID, 'publication_type')))
    #     publication_type_filter.click()
    #     option = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//option[text()='Journal']")))
    #     option.click()
    #     time.sleep(2)

    #     # Verifica que los resultados están filtrados por tipo de publicación
    #     results = self.driver.find_element(By.ID, 'results')
    #     for card in results.find_elements(By.CLASS_NAME, 'card'):
    #         self.assertIn("Journal", card.text)
    #     print("Filtro por tipo de publicación: OK")

    # def test_filter_by_author(self):
    #     author_filter = self.driver.find_element(By.ID, 'authors')
    #     self.driver.execute_script("arguments[0].scrollIntoView();", author_filter)
    #     self.wait.until(EC.element_to_be_clickable((By.ID, 'authors')))
    #     author_filter.click()
    #     option = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//option[text()='John Doe']")))
    #     option.click()
    #     time.sleep(2)

    #     # Verifica que los resultados están filtrados por autor
    #     results = self.driver.find_element(By.ID, 'results')
    #     for card in results.find_elements(By.CLASS_NAME, 'card'):
    #         self.assertIn("John Doe", card.text)
    #     print("Filtro por autor: OK")

    # def test_filter_by_files(self):
    #     files_filter = self.driver.find_element(By.ID, 'files')
    #     self.driver.execute_script("arguments[0].scrollIntoView();", files_filter)
    #     self.wait.until(EC.element_to_be_clickable((By.ID, 'files')))
    #     files_filter.click()
    #     option = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//option[text()='1file']")))
    #     option.click()
    #     time.sleep(2)

    #     # Verifica que los resultados están filtrados por número de archivos
    #     results = self.driver.find_element(By.ID, 'results')
    #     for card in results.find_elements(By.CLASS_NAME, 'card'):
    #         self.assertIn("1 file", card.text)
    #     print("Filtro por número de archivos: OK")

    # def test_filter_by_size(self):
    #     size_filter = self.driver.find_element(By.ID, 'size')
    #     self.driver.execute_script("arguments[0].scrollIntoView();", size_filter)
    #     self.wait.until(EC.element_to_be_clickable((By.ID, 'size')))
    #     size_filter.click()
    #     option = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//option[text()='lessThan1KB']")))
    #     option.click()
    #     time.sleep(2)

    #     # Verifica que los resultados están filtrados por tamaño
    #     results = self.driver.find_element(By.ID, 'results')
    #     for card in results.find_elements(By.CLASS_NAME, 'card'):
    #         self.assertIn("less than 1 KB", card.text)
    #     print("Filtro por tamaño: OK")

    # def test_filter_by_title(self):
    #     title_filter = self.driver.find_element(By.ID, 'title')
    #     self.driver.execute_script("arguments[0].scrollIntoView();", title_filter)
    #     self.wait.until(EC.element_to_be_clickable((By.ID, 'title')))
    #     title_filter.click()
    #     option = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//option[text()='Example Title']")))
    #     option.click()
    #     time.sleep(2)

    #     # Verifica que los resultados están filtrados por título
    #     results = self.driver.find_element(By.ID, 'results')
    #     for card in results.find_elements(By.CLASS_NAME, 'card'):
    #         self.assertIn("Example Title", card.text)
    #     print("Filtro por título: OK")

    # def test_filter_by_tag(self):
    #     tag_filter = self.driver.find_element(By.ID, 'tag')
    #     self.driver.execute_script("arguments[0].scrollIntoView();", tag_filter)
    #     self.wait.until(EC.element_to_be_clickable((By.ID, 'tag')))
    #     tag_filter.click()
    #     option = self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//option[text()='Example Tag']")))
    #     option.click()
    #     time.sleep(2)

    #     # Verifica que los resultados están filtrados por etiqueta
    #     results = self.driver.find_element(By.ID, 'results')
    #     for card in results.find_elements(By.CLASS_NAME, 'card'):
    #         self.assertIn("Example Tag", card.text)
    #     print("Filtro por etiqueta: OK")

    def test_clear_filters(self):
        clear_button = self.driver.find_element(By.ID, 'clear-filters')
        self.driver.execute_script("arguments[0].scrollIntoView();", clear_button)
        self.wait.until(EC.element_to_be_clickable((By.ID, 'clear-filters')))
        time.sleep(1)  # Espera adicional para asegurar que el elemento esté completamente cargado
        self.driver.execute_script("arguments[0].click();", clear_button)  # Usar JavaScript para hacer clic
        time.sleep(1)

        # Verifica que todos los filtros están en sus valores predeterminados
        self.assertEqual(self.driver.find_element(By.ID, 'authors').get_attribute('value'), 'any')
        self.assertEqual(self.driver.find_element(By.ID, 'query').get_attribute('value'), '')
        print("Limpieza de filtros: OK")

if __name__ == "__main__":
    unittest.main()