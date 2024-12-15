from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_dashboard_scroll_and_click():
    # Configuración inicial
    driver = webdriver.Chrome()
    base_url = "http://127.0.0.1:5000"  # Cambiar según el entorno
    driver.get(f"{base_url}/login")
    time.sleep(2)

    # Paso 1: Iniciar sesión
    driver.find_element(By.ID, "email").send_keys("user1@example.com")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.ID, "submit").click()
    time.sleep(2)

    # Paso 2: Navegar al Dashboard
    driver.get(f"{base_url}/dashboard")
    time.sleep(2)

    # Paso 3: Hacer clic en el primer "Latest Unsynchronized Dataset"
    print("Buscando el primer elemento de 'Latest Unsynchronized Datasets'...")
    try:
        dataset_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'unsynchronized')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", dataset_link)
        time.sleep(1)
        print("Haciendo clic en el primer 'Latest Unsynchronized Dataset'.")
        dataset_link.click()
        time.sleep(2)

        # Regresar a la página principal del Dashboard
        driver.get(f"{base_url}/dashboard")
        time.sleep(2)
        print("De regreso a la página principal del Dashboard.")

    except Exception as e:
        print(f"Error al interactuar con el primer 'Latest Unsynchronized Dataset': {e}")
        driver.quit()
        return

    # Paso 4: Scroll y clic en botones "Generar Gráfica"
    total_height = driver.execute_script("return document.body.scrollHeight")
    scroll_step = 200  # Tamaño del desplazamiento en píxeles
    current_scroll_position = 0

    buttons_clicked = 0  # Contador de botones
    print("Iniciando scroll y búsqueda de botones 'Generar Gráfica'...")

    while current_scroll_position < total_height:
        # Desplazar la página
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        current_scroll_position += scroll_step
        time.sleep(0.5)  # Scroll suave

        # Intentar encontrar botones visibles
        buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Generar Gráfica')]")

        for button in buttons:
            if button.is_displayed():
                try:
                    # Desplazar el botón al centro de la vista
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                    time.sleep(1)

                    # Esperar que el botón sea clicable y hacer clic
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
                    print("Haciendo clic en el botón 'Generar Gráfica'.")
                    button.click()
                    time.sleep(2)
                    buttons_clicked += 1

                    # Scroll al final después del segundo botón
                    if buttons_clicked == 2:
                        print("Desplazándose al final de la página...")
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)

                except Exception as e:
                    print(f"Error al hacer clic en el botón: {e}")

        if buttons_clicked >= 2:  # Detener después de 2 clics
            break

    print(f"Se hicieron clic en {buttons_clicked} botones 'Generar Gráfica'.")
    print("Test completado con éxito.")

    # Finalizar el test
    driver.quit()
