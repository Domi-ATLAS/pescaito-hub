from locust import HttpUser, TaskSet, task, between
from core.environment.host import get_host_for_locust_testing


class ExploreBehavior(TaskSet):
    def on_start(self):
        """
        Llamada inicial al endpoint para simular la preparación o inicio de sesión.
        """
        self.client.get("/")  # Simula acceder a la página principal

    @task(2)
    def explore_basic_search(self):
        """
        Simula una búsqueda básica en el endpoint /explore con una query simple.
        """
        response = self.client.get("/explore?query=example")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    @task(1)
    def explore_advanced_search(self):
        """
        Simula una búsqueda avanzada en el endpoint /explore con parámetros adicionales.
        """
        params = {"query": "advanced query", "sorting": "oldest", "tags": "tag1,tag2"}
        response = self.client.get("/explore", params=params)
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    @task(1)
    def explore_post_search(self):
        """
        Simula una petición POST en el endpoint /explore para enviar datos complejos.
        """
        payload = {"query": "example post query", "tags": ["tag1", "tag3"], "sorting": "newest"}
        response = self.client.post("/explore", json=payload)
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    @task(1)
    def explore_invalid_params(self):
        """
        Prueba negativa: Simula búsqueda avanzada con parámetros malformados.
        """
        params = {"query": None, "sorting": "invalid_sorting", "tags": "123,!!invalid"}
        response = self.client.get("/explore", params=params)
        assert response.status_code in [400, 422], f"Expected failure, got {response.status_code}"
        print("Handled invalid parameters gracefully.")

    @task(1)
    def explore_slow_response(self):
        """
        Prueba de rendimiento: Evalúa cómo maneja la aplicación una simulación de respuesta lenta.
        """
        with self.client.get(
            "/explore?query=slow_test",
            catch_response=True,
            timeout=10,
        ) as response:
            if response.elapsed.total_seconds() > 5:
                response.success()
                print(f"Warning: Slow response time: {response.elapsed.total_seconds()}s")
            else:
                response.failure(f"Unexpected fast response: {response.elapsed.total_seconds()}s")

    @task(1)
    def explore_large_payload(self):
        """
        Simula una petición POST con una carga de datos extremadamente grande.
        """
        payload = {
            "query": "large_payload_test",
            "tags": [f"tag{i}" for i in range(1000)],  # 1000 tags
            "sorting": "newest",
        }
        response = self.client.post("/explore", json=payload)
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        print("Successfully handled large payload.")


class ExploreUser(HttpUser):
    """
    Simula el comportamiento de un usuario accediendo a las rutas de exploración.
    """
    tasks = [ExploreBehavior]
    wait_time = between(5, 9)  # Espera entre 5 y 9 segundos entre solicitudes
    host = get_host_for_locust_testing()
