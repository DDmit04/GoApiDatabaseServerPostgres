from typing import Dict

from sqlalchemy.orm import Session

from my_types.config_object import ConfigObject
from my_types.transactional_object import TransactionalObject
from utils.database_utills import transactional
from model.databse_service_tables import DatabaseStatsTable


class LocalDatabaseRepository(TransactionalObject):

    def __init__(self, session: Session,
                 scripts_paths_config: ConfigObject,
                 schemas_config: ConfigObject):
        super().__init__(session)
        self.scripts_paths = scripts_paths_config
        self.schemas_config = schemas_config

    def exec_query(self, query: str) -> list[Dict]:
        res = self.session.execute(query).all()
        return [row._asdict() for row in res]

    def update_user_password(self, username: str, new_password: str):
        config = {
            'username': username,
            'password': new_password
        }
        self.__call_script_from_file(
            self.scripts_paths.get('target_update_user_password_script_name'),
            **config
        )

    def get_database_stats(self) -> DatabaseStatsTable:
        database_stats = self.session.query(DatabaseStatsTable).first()
        return database_stats

    @transactional
    def init_new_database(self, name: str, password: str,
                          database_stats: DatabaseStatsTable):
        self.__create_user(name, password, database_stats)
        self.__setup_database(name, database_stats)

    def update_database_size(self, new_size: int):
        self.session.query(DatabaseStatsTable).update(
            {DatabaseStatsTable.max_bytes: new_size}
        )

    def allow_database_external_connections(self, name: str):
        config = {
            'name': name
        }
        self.__call_script_from_file(
            self.scripts_paths.get('target_allow_connections_script_name'),
            **config
        )

    def forbid_database_external_connections(self, name: str):
        config = {
            'name': name
        }
        self.__call_script_from_file(
            self.scripts_paths.get('target_forbid_connections_script_name'),
            **config
        )

    def __setup_database(self, name, database_stats):
        protected_schema_name = self.schemas_config.get(
            'protected_schema_name')
        db_init_config = {
            'username': name,
            'maxSize': database_stats.max_bytes,
            'protectedSchemaName': protected_schema_name
        }
        stats_table_name = self.schemas_config.get(
            'database_stats_table_name'
        )
        service_table_name = self.schemas_config.get(
            'database_service_table_name'
        )
        full_db_stats_table_name = f"{protected_schema_name}.{stats_table_name}"
        full_db_service_table_name = f"{protected_schema_name}.{service_table_name}"
        triggers_init_config = {
            'privateSchemaName': protected_schema_name,
            'databaseStatsFullTableName': full_db_stats_table_name,
            'databaseServiceFullTableName': full_db_service_table_name,
        }
        self.__call_script_from_file(
            self.scripts_paths.get('target_init_db_script_name'),
            **db_init_config
        )
        self.__call_script_from_file(
            self.scripts_paths.get('target_create_db_triggers_script_name'),
            **triggers_init_config
        )

    def delete_user(self, username: str):
        remove_user_config = {
            "name": username
        }
        self.__call_script_from_file(
            self.scripts_paths.get('delete_user_script_name'),
            **remove_user_config
        )

    def __create_user(self, name, password, database_stats):
        self.session.add(database_stats)
        user_config = {
            'username': name,
            'password': password,
        }
        self.__call_script_from_file(
            self.scripts_paths.get('create_user_script_name'),
            **user_config
        )

    def __call_script_from_file(self, path: str, **kwargs: Dict):
        with(open(path, 'r')) as file:
            db_script = file.read()
            self.session.execute(db_script.format(**kwargs))
