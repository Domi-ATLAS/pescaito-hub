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

    def test_filter_by_publication_type(self):
        dropdown = self.driver.find_element(By.ID, "publication_type")
        dropdown.find_element(By.XPATH, "//option[. = 'Data Management Plan']").click()

        # Espera a que el elemento "Sample dataset 1" sea clickable
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sample dataset 1"))
        )

        # Desplazar la vista hasta el elemento si es necesario
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        # Hacer clic en el elemento
        element.click()

        print("Filtro por tipo de publicación: OK")
        
    def test_filter_by_author(self):
        dropdown = self.driver.find_element(By.ID, "authors")
        dropdown.find_element(By.XPATH, "//option[. = 'Author 1']").click()

        # Espera a que el elemento "Sample dataset 1" sea clickable
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sample dataset 1"))
        )

        # Desplazar la vista hasta el elemento si es necesario
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        # Hacer clic en el elemento
        element.click()

        print("Filtro por autor: OK")

    def test_filter_by_files(self):
        dropdown = self.driver.find_element(By.ID, "files")
        dropdown.find_element(By.XPATH, "//option[. = '3 Files']").click()

        # Espera a que el elemento "Sample dataset 1" sea clickable
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sample dataset 1"))
        )

        # Desplazar la vista hasta el elemento si es necesario
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        # Hacer clic en el elemento
        element.click()

        print("Filtro por archivos: OK")

    def test_filter_by_size(self):
        dropdown = self.driver.find_element(By.ID, "size")
        dropdown.find_element(By.XPATH, "//option[. = 'Between 1KB and 2KB']").click()

        # Espera a que el elemento "Sample dataset 1" sea clickable
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sample dataset 1"))
        )

        # Desplazar la vista hasta el elemento si es necesario
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        # Hacer clic en el elemento
        element.click()

        print("Filtro por tamaño: OK")

    def test_filter_by_title(self):
        dropdown = self.driver.find_element(By.ID, "title")
        dropdown.find_element(By.XPATH, "//option[. = 'Sample dataset 1']").click()

        # Espera a que el elemento "Sample dataset 1" sea clickable
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sample dataset 1"))
        )

        # Desplazar la vista hasta el elemento si es necesario
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        # Hacer clic en el elemento
        element.click()

        print("Filtro por titulo: OK")

    def test_filter_by_tag(self):

        dropdown = self.driver.find_element(By.ID, "tag")
        dropdown.find_element(By.XPATH, "//option[. = 'Any']").click()

        # Espera a que el elemento "Sample dataset 1" sea clickable
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sample dataset 1"))
        )

        # Desplazar la vista hasta el elemento si es necesario
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        # Hacer clic en el elemento
        element.click()

        print("Filtro por tag: OK")

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