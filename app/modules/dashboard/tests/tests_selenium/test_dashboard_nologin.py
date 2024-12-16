from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestHomeToDashboardScroll:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.base_url = "http://localhost:5000"

    def teardown_method(self, method):
        self.driver.quit()

    def test_home_to_dashboard_scroll(self):
        driver = self.driver

        # Paso 1: Acceder a la página principal (Home)
        driver.get(self.base_url)
        time.sleep(2)
        print("Página de inicio (Home) cargada correctamente.")

        # Paso 2: Navegar al Dashboard desde Home
        try:
            dashboard_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Dashboard"))
            )
            print("Haciendo clic en el enlace 'Dashboard'.")
            dashboard_link.click()
        except Exception as e:
            print(f"No se encontró el enlace 'Dashboard': {e}")

        # Paso 3: Verificar redirección o realizar scroll en Dashboard
        current_url = driver.current_url
        if "/login" in current_url:
            print("El acceso al Dashboard redirigió correctamente a la página de inicio de sesión.")
        else:
            print("No se redirigió al inicio de sesión. Realizando scroll en el Dashboard...")

            # Realizar scroll en la página del Dashboard
            total_height = driver.execute_script("return document.body.scrollHeight")
            scroll_step = 200  # Tamaño del desplazamiento en píxeles
            current_scroll_position = 0

            while current_scroll_position < total_height:
                driver.execute_script(f"window.scrollBy(0, {scroll_step});")
                current_scroll_position += scroll_step
                time.sleep(0.5)  # Scroll suave

            print("Scroll completado en la página del Dashboard.")
