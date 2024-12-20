# Generated by Selenium IDE
import pytest
import time
import os
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestCreateDataset():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.base_url = "http://localhost:5000"
  
    def teardown_method(self, method):
        self.driver.quit()
  
    def test_create_dataset(self):
        # Paso 1: Iniciar sesión
        self.driver.get(f"{self.base_url}/login")
        time.sleep(2)
        self.driver.set_window_size(912, 1011)
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(2)

        # Paso 2: Navegar a "Mis Datasets"
        self.driver.get(f"{self.base_url}/dataset/list")
        time.sleep(2)

        # Capturar la lista inicial de datasets
        initial_datasets = self.driver.find_elements(By.XPATH, "//table/tbody/tr")
        initial_count = len(initial_datasets)

        # Paso 3: Seleccionar modelos de características
        self.driver.get(f"{self.base_url}/cart/select_models")
        time.sleep(2)
        self.driver.find_element(By.ID, "model_5").click()
        self.driver.find_element(By.ID, "model_6").click()
        self.driver.find_element(By.ID, "model_8").click()
        self.driver.find_element(By.ID, "add-to-cart-btn").click()
        time.sleep(2)

        # Paso 4: Crear el dataset
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Create Dataset')]").click()
        time.sleep(2)

        # Paso 5: Validar cambios en la lista de datasets
        self.driver.get(f"{self.base_url}/dataset/list")
        time.sleep(2)

        new_datasets = self.driver.find_elements(By.XPATH, "//table/tbody/tr")
        new_count = len(new_datasets)

        assert new_count > initial_count, "El dataset no fue agregado a la lista."
        print("El dataset fue creado exitosamente y está en la lista.")

