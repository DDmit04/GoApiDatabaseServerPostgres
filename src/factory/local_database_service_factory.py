from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from my_types.config_object import ConfigObject
from repo.local_database_repo import LocalDatabaseRepository
from service.local_database_service import LocalDatabaseService


class LocalDatabaseServiceFactory:

    def __init__(self, scripts_paths: ConfigObject,
                 schemas_config: ConfigObject):
        super().__init__()
        self._scripts_paths = scripts_paths
        self._schemas_config = schemas_config

    def get_local_database_service(self, engine: Engine) -> \
            LocalDatabaseService:
        Session = sessionmaker(bind=engine)
        session = Session()
        repository = LocalDatabaseRepository(
            session,
            self._scripts_paths,
            self._schemas_config
        )
        return LocalDatabaseService(repository)
