from sqlalchemy import Column, Integer, String, UniqueConstraint, Boolean
from sqlalchemy.orm import declarative_base

from injector.config.config_loader_container import config_container

app_database_model = declarative_base()

tables_schema_config = config_container.get_tables_schema_config()
app_databases_table_name = tables_schema_config.get(
    'app_databases_table_name')


class Database(app_database_model):
    __tablename__ = app_databases_table_name
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    real_db_id = Column(Integer, nullable=False)
    db_size = Column(Integer, nullable=False)
    allow_connections = Column(Boolean, nullable=False, default=True)
    __table_args__ = (
        UniqueConstraint("name", name='name_unique'),
        UniqueConstraint("real_db_id", name='db_id_unique')
    )
