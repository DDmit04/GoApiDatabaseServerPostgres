from sqlalchemy.engine import Engine

from model.databse_service_tables import local_database_model
from my_types.config_object import ConfigObject
from utils.database_utills import create_database_tables, \
    create_database_engine


class LocalDatabaseEngineFactory:

    def __init__(self, local_database_config: ConfigObject):
        self._local_database_config = local_database_config
        self.engine: Engine = None

    def __call__(self, db_name):
        db_url = self._local_database_config.get('DB_URL')
        echo_enabled = self._local_database_config.get('ECHO')
        self.engine = create_database_engine(db_url, echo_enabled, db_name)
        return self

    def create_database_tables(self):
        if self.engine is not None:
            create_database_tables(self.engine, local_database_model)
        else:
            # TODO raise
            pass

    def __enter__(self):
        return self.engine

    def __exit__(self, type, value, traceback):
        self.engine.dispose()
