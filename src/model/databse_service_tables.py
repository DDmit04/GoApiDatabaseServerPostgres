from sqlalchemy import Column, Integer, String, Boolean, ARRAY, Unicode, \
    UniqueConstraint
from sqlalchemy.orm import declarative_base

from injector.config.config_loader_container import config_container

local_database_model = declarative_base()

tables_schema_config = config_container.get_tables_schema_config()
protected_schema_name = tables_schema_config.get('protected_schema_name')
database_stats_table_name = tables_schema_config \
    .get('database_stats_table_name')
database_service_table_name = tables_schema_config \
    .get('database_service_table_name')


class DatabaseStatsTable(local_database_model):
    __tablename__ = database_stats_table_name
    __table_args__ = (
        UniqueConstraint("one_id"),
        {"schema": protected_schema_name}
    )
    one_id = Column(Boolean, primary_key=True, default=True)
    max_bytes = Column(Integer, default=0)
    current_bytes = Column(Integer, default=0)
    fill_percent = Column(Integer, default=0)


class DatabaseServiceTable(local_database_model):
    __tablename__ = database_service_table_name
    __table_args__ = (
        UniqueConstraint("table_id"),
        {"schema": protected_schema_name}
    )
    id = Column(Integer, primary_key=True)
    table_id = Column(String, nullable=False, unique=True)
    trigger_names = Column(ARRAY(Unicode))
