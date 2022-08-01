from dataclasses import dataclass

from sqlalchemy.orm import Session, sessionmaker

from exception.transaction.session_not_found_exception import \
    SessionNotFoundException
from factory.local_database_engine_factory import LocalDatabaseEngineFactory
from factory.local_database_service_factory import LocalDatabaseServiceFactory
from injector.config.config_loader_container import config_container
from model.databse_service_tables import DatabaseServiceTable, local_database_model
from repo.app_database_repo import AppDatabaseRepository
from service.app_database_service import AppDatabaseService
from service.database_service_facade import DatabaseServiceFacade
from service.server.grpc_server_service import GrpcServerService
from service.server.server_register_service import ServerRegisterService
from model.database_table import app_database_model
from utils.database_utills import create_database_engine, \
    create_database_tables


@dataclass
class SessionRecord:
    session_id: str
    session: Session


class DefaultDependencyInjector:

    def __init__(self):
        super().__init__()
        self._app_sessions_pool: list[SessionRecord] = []

    def get_app_database_repo(self, session_id: str):
        session = self.get_app_database_session(session_id)
        return AppDatabaseRepository(session)

    def get_local_database_service_factory(self):
        scripts_config = config_container.get_sql_scripts_config()
        schemas_config = config_container.get_tables_schema_config()
        return LocalDatabaseServiceFactory(scripts_config, schemas_config)

    def get_local_database_engine_factory(self):
        config = config_container.get_local_database_config()
        return LocalDatabaseEngineFactory(config)

    def get_grpc_server_service(self):
        server_config = config_container.get_server_config()
        return GrpcServerService(
            server_config
        )

    def get_app_database_service(self, session_id):
        session = self.get_app_database_session(session_id)
        app_database_repo = self.get_app_database_repo(session_id)
        name_length = config_container.get_common_config().get('name_length')
        return AppDatabaseService(session, app_database_repo, name_length)

    def get_server_register_service(self, session_id):
        server_config = config_container.get_server_config()
        db_type = config_container.get_common_config().get('database_type')
        app_database_service = self.get_app_database_service(session_id)
        return ServerRegisterService(
            app_database_service,
            server_config,
            db_type
        )

    def get_database_service(self):
        return DatabaseServiceTable(local_database_model)

    def get_database_service_facade(self, session_id):
        session = self.get_app_database_session(session_id)
        engine_factory = self.get_local_database_engine_factory()
        service_factory = self.get_local_database_service_factory()
        app_database_service = self.get_app_database_service(session_id)
        database_service = self.get_database_service()
        return DatabaseServiceFacade(
            session,
            app_database_service,
            database_service,
            service_factory,
            engine_factory
        )

    def get_app_database_session(self, session_id: str) -> Session:
        existing_session_record: SessionRecord = self \
            .__find_app_session_by_id(session_id)
        if existing_session_record is None:
            session = self.__create_new_app_database_session()
            self._app_sessions_pool.append(SessionRecord(session_id, session))
            session.begin()
            return session
        return existing_session_record.session

    def close_app_database_session(self, session_id):
        existing_session_record: SessionRecord = self \
            .__find_app_session_by_id(session_id)
        if existing_session_record is None:
            raise SessionNotFoundException()
        session: Session = existing_session_record.session
        session.commit()
        session.close()
        self._app_sessions_pool.remove(existing_session_record)

    def __create_new_app_database_session(self) -> Session:
        config = config_container.get_app_database_config()
        db_url = config.get('DB_URL')
        echo = config.get('ECHO')
        engine = create_database_engine(db_url, echo)
        create_database_tables(engine, app_database_model)
        session_maker: sessionmaker = sessionmaker(bind=engine)
        session: Session = session_maker()
        return session

    def __find_app_session_by_id(self, session_id) -> SessionRecord:
        for existing_session in self._app_sessions_pool:
            if existing_session.session_id == session_id:
                return existing_session
        return None
