from sqlalchemy.engine import Engine
from sqlalchemy_utils import create_database, drop_database

from utils.database_utills import create_database_tables


class ServerDatabaseService:

    def __init__(self, model):
        self.model = model
        super().__init__()

    def create_database(self, engine: Engine):
        create_database(engine.url)
        create_database_tables(engine, self.model)

    def drop_database(self, engine: Engine):
        drop_database(engine.url)
