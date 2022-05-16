from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, ARRAY, Unicode

target_metadata = MetaData()

control = Table(
    'control', target_metadata,
    Column('one_id', Boolean, primary_key=True, default=True),
    Column('max_bytes', Integer, default=0),
    Column('current_bytes', Integer, default=0),
    Column('fill_percent', Integer, default=0),
    Column('user_schema_names', ARRAY(Unicode)),
)
control_table = Table(
    'control_table', target_metadata,
    Column('id', Integer, primary_key=True),
    Column('table_id', String, nullable=False, unique=True),
    Column('trigger_names', ARRAY(Unicode)),
)
