from locust import HttpUser, TaskSet, task
from random import randint
from core.locust.common import get_csrf_token
from core.environment.host import get_host_for_locust_testing

class DatasetBehavior(TaskSet):
    def on_start(self):
        self.dataset()

    @task
    def dataset(self):
        response = self.client.get("/dataset/upload")
        get_csrf_token(response)

    @task
    def rate_dataset(self):
        # Usamos un rango de dataset_ids, puedes modificar el rango según lo necesites
        dataset_ids = [1, 2, 3, 4, 5]  # Cambia esto con los dataset_ids que quieras probar
        
        # Seleccionamos un dataset_id aleatorio
        dataset_id = dataset_ids[randint(0, len(dataset_ids) - 1)]
        rating = randint(1, 5)  # Generamos un rating aleatorio entre 1 y 5
        
        # Realizamos la solicitud POST para actualizar el rating
        response = self.client.post(
            f"/dataset/{dataset_id}/update_rating/{rating}",
            headers={"Content-Type": "application/json"}  # Asegúrate de que el header sea el correcto
        )
        
        if response.status_code == 200:
            print(f"Rating actualizado a {rating} para el dataset {dataset_id}")
        else:
            print(f"Error al actualizar el rating para el dataset {dataset_id}: {response.text}")

class DatasetUser(HttpUser):
    tasks = [DatasetBehavior]
    min_wait = 5000  # Tiempo mínimo de espera entre tareas (5 segundos)
    max_wait = 9000  # Tiempo máximo de espera entre tareas (9 segundos)
    host = get_host_for_locust_testing()
