from sqlalchemy import select, update, insert

import Config
from App.utils.DbUtils import transactional_class_method
from App.tables.DatabseStatsTable import control


def call_script_from_file(session, path, **kwargs):
    with(open(path, 'r')) as file:
        db_script = file.read()
        session.execute(db_script.format(**kwargs))


class TargetDatabaseRepository:

    @transactional_class_method
    def exec_target_user_query(self, session, query):
        session.execute("set schema 'user_dbs';")
        aw = session.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'user_dbs';")
        res = session.execute(query)
        return [r._asdict() for r in res.all()]

    @transactional_class_method
    def update_user_password(self, session, username, new_password):
        config = {
            'username': username,
            'password': new_password
        }
        call_script_from_file(session, Config.sql_scripts_paths['TARGET_UPDATE_USER_PASSWORD_SCRIPT_PATH'], **config)

    @transactional_class_method
    def get_database_stats(self, session):
        query = select(control)
        res = session.execute(query)
        return dict(res.first())

    @transactional_class_method
    def init_new_database(self, session, username, password, size):
        insert_query = insert(control).values(
            one_id=True,
            max_bytes=size,
            user_schema_names=['user_dbs'],
            fill_percent=0,
            current_bytes=0
        )
        session.execute(insert_query)
        user_config = {
            'username': username,
            'password': password,
        }
        call_script_from_file(session, Config.sql_scripts_paths['CREATE_USER_SCRIPT_PATH'], **user_config)
        db_init_config = {
            'username': username,
            'maxSize': size
        }
        call_script_from_file(session, Config.sql_scripts_paths['TARGET_INIT_DB_SCRIPT_PATH'], **db_init_config)
        call_script_from_file(session, Config.sql_scripts_paths['TARGET_CREATE_DB_TRIGGERS_SCRIPT_PATH'])

    @transactional_class_method
    def update_database_size(self, session, new_size):
        update_query = update(control).values(max_bytes=new_size)
        session.execute(update_query)
