from sqlalchemy import func
from app.modules.dataset.repositories import AuthorRepository, DSDownloadRecordRepository, DSMetaDataRepository, DSViewRecordRepository, DataSetRepository
from app.modules.featuremodel.repositories import FMMetaDataRepository, FeatureModelRepository
from app.modules.hubfile.repositories import HubfileDownloadRecordRepository, HubfileRepository, HubfileViewRecordRepository
from core.services.BaseService import BaseService


class DataSetService(BaseService):
    def __init__(self):
        super().__init__(DataSetRepository())
        self.feature_model_repository = FeatureModelRepository()
        self.author_repository = AuthorRepository()
        self.dsmetadata_repository = DSMetaDataRepository()
        self.fmmetadata_repository = FMMetaDataRepository()
        self.dsdownloadrecord_repository = DSDownloadRecordRepository()
        self.hubfiledownloadrecord_repository = HubfileDownloadRecordRepository()
        self.hubfilerepository = HubfileRepository()
        self.dsviewrecord_repostory = DSViewRecordRepository()
        self.hubfileviewrecord_repository = HubfileViewRecordRepository()


    def count_unsynchronized_datasets(self):
        return self.repository.count_unsynchronized_datasets()