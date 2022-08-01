from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql.ddl import CreateSchema

from exception.transaction.transactional_exception import \
    TransactionalException
from my_types.transactional_object import TransactionalObject


def transactional(func):
    def wrapper(self, *args, **kwargs):
        if not isinstance(self, TransactionalObject):
            raise TransactionalException("Call transactional method "
                                         "outside transactional object!")
        transactional_service: TransactionalObject = self
        transaction = transactional_service.session.begin_nested()
        try:
            res = func(self, *args, **kwargs)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e
        return res

    return wrapper


def create_database_engine(url: str, echo=True, database_name: str = None) \
        -> Engine:
    if database_name is not None:
        url += f"/{database_name}"
    engine = create_engine(url, echo=echo)
    return engine


def create_database_tables(engine: Engine, model):
    tables = model.metadata.tables
    created_schemas = []
    for table_name, table_data in tables.items():
        table_schema = table_data.schema
        name_not_blank = not (table_schema == '' or table_schema is None)
        schema_created = created_schemas.count(table_schema) > 0
        if name_not_blank and not schema_created:
            engine.execute(CreateSchema(table_schema))
            created_schemas.append(table_schema)
    model.metadata.create_all(engine)
