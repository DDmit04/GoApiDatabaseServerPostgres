from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from App.tables.DatabaseTable import server_metadata
from App.tables.DatabseStatsTable import target_metadata


def construct_db_url(db_type, host, username, password, db_name):
    return f"{db_type}://{username}:{password}@{host}/{db_name}"


def get_db_session_factory(engine, is_user_database=False):
    if is_user_database:
        target_metadata.create_all(engine)
    else:
        server_metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(engine)
    return Session


def get_server_session_factory(engine):
    return get_db_session_factory(engine)


def get_user_session_factory(engine):
    return get_db_session_factory(engine, True)


def get_db_engine(config):
    return get_db_engine_by_name(config, config['DB_NAME'])


def get_db_engine_by_name(config, db_name):
    db_type = config['DB_TYPE']
    host = config['DB_HOST']
    username = config['DB_USERNAME']
    password = config['DB_PASSWORD']
    db_url = construct_db_url(db_type, host, username, password, db_name)
    engine = create_engine(db_url, echo=True)
    return engine
