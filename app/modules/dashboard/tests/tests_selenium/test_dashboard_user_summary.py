from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestExportUserSummaryPDF:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.base_url = "http://localhost:5000"  # Cambiar según el entorno

    def teardown_method(self, method):
        self.driver.quit()

    def test_export_user_summary_pdf_with_scroll(self):
        driver = self.driver

        # Paso 1: Iniciar sesión
        driver.get(f"{self.base_url}/login")
        time.sleep(2)
        driver.find_element(By.ID, "email").send_keys("user1@example.com")
        driver.find_element(By.ID, "password").send_keys("1234")
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)

        # Paso 2: Navegar al Dashboard
        driver.get(f"{self.base_url}/dashboard")
        time.sleep(2)

        # Paso 3: Scroll hasta el botón "Export User Summary as PDF"
        print("Buscando el botón 'Export User Summary as PDF'...")
        try:
            # Encontrar el botón y desplazarlo al centro de la vista
            export_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Export User Summary as PDF"))
            )
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", export_button)
            time.sleep(1)

            # Esperar que el botón sea clicable y hacer clic
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(export_button))
            print("Haciendo clic en el botón 'Export User Summary as PDF'.")
            export_button.click()
            time.sleep(2)

            # Verificar que estamos en la URL del visor del PDF
            current_url = driver.current_url
            assert "/dashboard/export_user_summary" in current_url, f"La URL del PDF no es correcta: {current_url}"
            print("El visor del PDF se ha abierto correctamente.")

            # Paso 4: Ver la primera página del PDF
            print("Desplazándose a la primera página del PDF...")
            driver.execute_script("window.scrollTo(0, 0);")  # Ir al inicio (primera página)
            time.sleep(2)  # Espera para visualización
            print("Primera página del PDF visible.")

            # Paso 5: Desplazarse a la segunda página del PDF
            print("Desplazándose a la segunda página del PDF...")
            total_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script(f"window.scrollTo(0, {total_height / 2});")  # Scroll a la mitad de la página
            time.sleep(2)  # Espera para visualización
            print("Segunda página del PDF visible.")

        except Exception as e:
            print(f"Error durante la prueba: {e}")
