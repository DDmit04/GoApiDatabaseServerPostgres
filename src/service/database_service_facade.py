from typing import Dict

from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists

from controller.dto.database_stats_dto import DatabaseStatsDto
from exception.database_id_already_exists_exception import \
    DatabaseIdAlreadyExistsException
from exception.database_name_already_exists_exception import \
    DatabaseNameAlreadyExistsException
from exception.invalid_database_size_exception import \
    InvalidDatabaseSizeException
from factory.local_database_engine_factory import \
    LocalDatabaseEngineFactory
from factory.local_database_service_factory import \
    LocalDatabaseServiceFactory
from model.database_table import Database
from my_types.transactional_object import TransactionalObject
from service.app_database_service import AppDatabaseService
from service.server.server_database_service import ServerDatabaseService
from utils.database_utills import transactional


class DatabaseServiceFacade(TransactionalObject):

    def __init__(self, session: Session,
                 app_database_service: AppDatabaseService,
                 database_service: ServerDatabaseService,
                 local_database_service_factory: LocalDatabaseServiceFactory,
                 local_database_engine_factory: LocalDatabaseEngineFactory):
        super().__init__(session)
        self._app_database_service = app_database_service
        self._database_service = database_service
        self._local_database_service_factory = local_database_service_factory
        self._local_database_engine_factory = local_database_engine_factory

    @transactional
    def exec_user_query(self, db_id: int, query: str) -> list[Dict]:
        database = self._app_database_service \
            .get_database_info(db_id)
        database_name = database.name
        with self._local_database_engine_factory(database_name) as engine:
            service = self._local_database_service_factory \
                .get_local_database_service(engine)
            query_res = service.exec_query(query)
        return query_res

    @transactional
    def create_user_database(self, db_id: int, password: str, db_size: int) \
            -> DatabaseStatsDto:
        db_exists = self._app_database_service \
            .check_database_exists_by_database_id(db_id)
        if not db_exists:
            name = self._app_database_service.get_new_database_name()
            with self._local_database_engine_factory(name) as engine:
                new_db_url = engine.url
                is_real_db_exists = database_exists(new_db_url)
                if not is_real_db_exists:
                    self._database_service \
                        .create_database(engine)
                    try:
                        service = self._local_database_service_factory \
                            .get_local_database_service(engine)
                        service.init_new_database(
                            name, password, db_size
                        )
                        stats = service.get_database_stats()
                        self._app_database_service.add_new_database_info(
                            name, db_id, db_size
                        )
                        return stats
                    except Exception as e:
                        self._database_service.drop_database(engine)
                        raise e
                    return DatabaseStatsDto(0, 0, name, True)
                else:
                    raise DatabaseNameAlreadyExistsException(name)
        else:
            raise DatabaseIdAlreadyExistsException(db_id)

    @transactional
    def drop_database(self, db_id: int) -> Database:
        db_to_drop: Database = \
            self._app_database_service.get_database_info(db_id)
        name = db_to_drop.name
        self._app_database_service.remove_database_info(db_id)
        with self._local_database_engine_factory(name) as engine:
            service = self._local_database_service_factory \
                .get_local_database_service(engine)
            service.drop_user(name)
            self._database_service.drop_database(engine)

    @transactional
    def reset_database(self, db_id: int, password: str) -> Database:
        deleted_database: Database = self.drop_database(db_id)
        deleted_db_size = deleted_database.db_size
        database: Database = self.create_user_database(
            db_id, password, deleted_db_size
        )
        return database

    @transactional
    def update_database_size(self, db_id: int, new_size: int) -> bool:
        db_to_update: Database = self._app_database_service \
            .get_database_info(db_id)
        name = db_to_update.name
        with self._local_database_engine_factory(name) as engine:
            service = self._local_database_service_factory \
                .get_local_database_service(engine)
            stats = service.get_database_stats()
            current_size = stats.current_bytes
            is_valid = current_size < new_size
            if is_valid:
                service.update_database_size(new_size)
                self._app_database_service.update_database_size_info(new_size)
            else:
                raise InvalidDatabaseSizeException(db_id, new_size)
            return is_valid

    @transactional
    def update_database_password(self, db_id: int, new_password: str) -> bool:
        db_to_update: Database = self._app_database_service \
            .get_database_info(db_id)
        name = db_to_update.name
        with self._local_database_engine_factory(name) as engine:
            service = self._local_database_service_factory \
                .get_local_database_service(engine)
            service.update_database_password(name, new_password)
            return True

    @transactional
    def get_database_stats(self, db_id: int) -> DatabaseStatsDto:
        target_db: Database = self._app_database_service \
            .get_database_info(db_id)
        name: str = target_db.name
        with self._local_database_engine_factory(name) as engine:
            service = self._local_database_service_factory \
                .get_local_database_service(engine)
            database_stats = service.get_database_stats()
            statsDto: DatabaseStatsDto = DatabaseStatsDto(
                database_stats.fill_percent,
                database_stats.current_bytes
            )
            return statsDto

    @transactional
    def change_allow_connections(self, db_id: int, allow: bool):
        target_db: Database = self._app_database_service \
            .get_database_info(db_id)
        name: str = target_db.name
        with self._local_database_engine_factory(name) as engine:
            service = self._local_database_service_factory \
                .get_local_database_service(engine)
            if allow:
                service.allow_external_connections()
            else:
                service.forbid_external_connections()
