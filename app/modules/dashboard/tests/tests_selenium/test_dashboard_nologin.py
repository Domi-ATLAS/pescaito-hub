from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_home_to_dashboard_scroll():
    # Configuración inicial
    driver = webdriver.Chrome()
    base_url = "http://127.0.0.1:5000"  # Cambiar según el entorno

    # Paso 1: Acceder a la página principal (Home)
    driver.get(base_url)
    time.sleep(2)
    print("Página de inicio (Home) cargada correctamente.")

    # Paso 2: Navegar al Dashboard desde Home
    try:
        dashboard_link = driver.find_element(By.LINK_TEXT, "Dashboard")  # Cambiar según el texto del enlace en Home
        print("Haciendo clic en el enlace 'Dashboard'.")
        dashboard_link.click()
        time.sleep(2)
    except Exception as e:
        print(f"No se encontró el enlace 'Dashboard' en la página Home: {e}")
        driver.quit()
        return

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

    # Finalizar el test
    driver.quit()
