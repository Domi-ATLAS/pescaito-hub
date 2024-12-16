from app.modules.dashboard.models import Dashboard
from core.repositories.BaseRepository import BaseRepository


class DashboardRepository(BaseRepository):
    def __init__(self):
        super().__init__(Dashboard)