from typing import Dict

from repo.local_database_repo import LocalDatabaseRepository
from model.databse_service_tables import DatabaseStatsTable


class LocalDatabaseService:

    def __init__(self, local_database_repo: LocalDatabaseRepository):
        super().__init__()
        self._local_database_repo = local_database_repo

    def exec_query(self, query: str) \
            -> list[Dict]:
        return self._local_database_repo.exec_query(query)

    def init_new_database(self, name: str, password: str,
                          db_size: int):
        new_db_stats: DatabaseStatsTable = DatabaseStatsTable(
            one_id=True,
            max_bytes=db_size
        )
        self._local_database_repo.init_new_database(
            name, password, new_db_stats
        )

    def drop_user(self, name):
        self._local_database_repo.delete_user(name)

    def get_database_stats(self) -> DatabaseStatsTable:
        return self._local_database_repo.get_database_stats()

    def update_database_size(self, new_size):
        self._local_database_repo.update_database_size(new_size)

    def update_database_password(self, name, new_password):
        self._local_database_repo.update_user_password(name, new_password)

    def allow_external_connections(self):
        self._local_database_repo.allow_database_external_connections()

    def forbid_external_connections(self):
        self._local_database_repo.forbid_database_external_connections()
