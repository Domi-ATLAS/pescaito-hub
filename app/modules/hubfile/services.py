import os
import shutil
from flask_login import current_user  # Importación para obtener el usuario autenticado
from app.modules.auth.models import User
from app.modules.dataset.models import DataSet
from app.modules.hubfile.models import Hubfile
from app.modules.hubfile.repositories import (
    HubfileDownloadRecordRepository,
    HubfileRepository,
    HubfileViewRecordRepository
)
from core.services.BaseService import BaseService


class HubfileService(BaseService):
    def __init__(self):
        super().__init__(HubfileRepository())
        self.hubfile_view_record_repository = HubfileViewRecordRepository()
        self.hubfile_download_record_repository = HubfileDownloadRecordRepository()

    def get_owner_user_by_hubfile(self, hubfile: Hubfile) -> User:
        return self.repository.get_owner_user_by_hubfile(hubfile)

    def get_dataset_by_hubfile(self, hubfile: Hubfile) -> DataSet:
        return self.repository.get_dataset_by_hubfile(hubfile)

    def get_path_by_hubfile(self, hubfile: Hubfile) -> str:
        hubfile_user = self.get_owner_user_by_hubfile(hubfile)
        hubfile_dataset = self.get_dataset_by_hubfile(hubfile)
        working_dir = os.getenv('WORKING_DIR')

        path = os.path.join(working_dir,
                            'uploads',
                            f'user_{hubfile_user.id}',
                            f'dataset_{hubfile_dataset.id}',
                            hubfile.name)

        return path

    def total_hubfile_views(self) -> int:
        return self.hubfile_view_record_repository.total_hubfile_views()

    def total_hubfile_downloads(self) -> int:
        hubfile_download_record_repository = HubfileDownloadRecordRepository()
        return hubfile_download_record_repository.total_hubfile_downloads()
    
    def move_files_to_dataset_directory(self, dataset: DataSet):
        """
        Mueve todos los archivos de los FeatureModels seleccionados a la carpeta del dataset.
        """
        # Utilizamos current_user para obtener el usuario autenticado actual
        source_dir = current_user.temp_folder()  # Necesitamos definir el método temp_folder en el modelo User
        dest_dir = os.path.join(os.getenv('WORKING_DIR', ''),
                                'uploads',
                                f'user_{current_user.id}',
                                f'dataset_{dataset.id}')
        
        # Creamos el directorio si no existe
        os.makedirs(dest_dir, exist_ok=True)

        # Mover todos los archivos desde el directorio de origen al destino
        for feature_model in dataset.feature_models:
            for hubfile in feature_model.files:
                source_path = os.path.join(source_dir, hubfile.name)
                dest_path = os.path.join(dest_dir, hubfile.name)

                if os.path.exists(source_path):
                    shutil.move(source_path, dest_path)
                    print(f"Archivo movido: {source_path} -> {dest_path}")
                else:
                    print(f"Archivo no encontrado: {source_path}")



class HubfileDownloadRecordService(BaseService):
    def __init__(self):
        super().__init__(HubfileDownloadRecordRepository())
