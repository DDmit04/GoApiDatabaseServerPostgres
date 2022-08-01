import string
import random

from sqlalchemy.orm import Session

from exception.database_not_found_exception import DatabaseNotFoundException
from my_types.transactional_object import TransactionalObject
from repo.app_database_repo import AppDatabaseRepository
from model.database_table import Database


class AppDatabaseService(TransactionalObject):

    def __init__(self, session: Session,
                 database_repo: AppDatabaseRepository,
                 max_name_length: int):
        super().__init__(session)
        self._app_databases_repo = database_repo
        self._max_name_length = max_name_length

    def get_all_databases_info(self) -> list[Database]:
        databases: list[Database] = self._app_databases_repo.get_databases()
        return databases

    def get_database_info(self, db_id):
        database: Database = self._app_databases_repo \
            .get_database_by_database_id(db_id)
        if database is None:
            raise DatabaseNotFoundException(db_id)
        return database

    def check_database_exists_by_database_id(self, db_id) -> bool:
        exists = self._app_databases_repo.is_database_exists_by_real_id(db_id)
        return exists

    def get_new_database_name(self) -> str:
        name: str = ''.join(
            random.choices(
                string.ascii_lowercase, k=self._max_name_length
            )
        )
        database_by_name = \
            self._app_databases_repo.get_database_by_name(name)
        db_exists: bool = database_by_name is not None
        while db_exists:
            name = random.choices(string.ascii_lowercase)
            database_by_name = self.get_database_by_name(self.session, name)
            db_exists = database_by_name is not None
        return name

    def add_new_database_info(self, name, db_id, db_size):
        new_database = Database(
            name=name,
            real_db_id=db_id,
            db_size=db_size
        )
        self._app_databases_repo.add_database(new_database)

    def remove_database_info(self, db_id):
        self._app_databases_repo.remove_database(db_id)

    def update_database_size_info(self, new_size):
        self._app_databases_repo.update_database_size(new_size)
