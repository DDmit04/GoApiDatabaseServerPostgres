from sqlalchemy.orm import Session

from exception.database_not_found_exception import DatabaseNotFoundException
from model.database_table import Database
from my_types.transactional_object import TransactionalObject


class AppDatabaseRepository(TransactionalObject):

    def __init__(self, session: Session):
        super().__init__(session)

    def get_databases(self) -> list[Database]:
        databases: list[Database] = self.session.query(Database).all()
        return databases

    def add_database(self, new_database: Database):
        self.session.add(new_database)

    def remove_database(self, real_db_id: int):
        self.session.query(Database).filter(
            Database.real_db_id == real_db_id).delete()

    def update_database_size(self, real_db_id: int, new_size: int):
        self.session.query(Database).filter(
            Database.real_db_id == real_db_id).update(
            {Database.db_size: new_size})

    def is_database_exists_by_real_id(self, real_db_id: int) -> bool:
        database: Database = self.session.query(Database).filter(
            Database.real_db_id == real_db_id).first()
        return database is not None

    def is_database_exists_by_name(self, name: str) -> bool:
        database: Database = self.session.query(Database).filter(
            Database.name == name).first()
        return database is not None

    def get_database_by_database_id(self, real_db_id: int) -> Database:
        database: Database = self.session.query(Database).filter(
            Database.real_db_id == real_db_id).first()
        return database

    def get_database_by_name(self, name: str) -> Database:
        database: Database = self.session.query(Database).filter(
            Database.name == name).first()
        return database
