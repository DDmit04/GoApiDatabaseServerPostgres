from sqlalchemy import MetaData, Table, Column, Integer, String, UniqueConstraint

server_metadata = MetaData()

database = Table(
    'user_database', server_metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(255), nullable=False, unique=True),
    Column('db_id', Integer, nullable=False),
    Column('db_size', Integer, nullable=False),
    Column('db_name', String(255), nullable=False, unique=True),
    UniqueConstraint('db_id', 'db_name', 'username', name='uix_1')
)
