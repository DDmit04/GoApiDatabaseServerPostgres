import os
from typing import Dict

import yaml
from yaml import SafeLoader

from my_types.config_object import ConfigObject


class ConfigLoader:

    def __init__(self, config_filepath: str) -> None:
        super().__init__()
        self._config_filepath = config_filepath

    def get_tables_schema_config(self):
        full_config = self.__load_config()
        schema_config = full_config['database']['schema']
        return self.__create_config_object(schema_config)

    def get_common_config(self):
        full_config = self.__load_config()
        config = full_config['common']
        return self.__create_config_object(config)

    def get_server_config(self):
        full_config = self.__load_config()
        config = full_config['server']
        return self.__create_config_object(config)

    def get_sql_scripts_config(self) -> Dict:
        full_config = self.__load_config()
        sql_scripts_config = full_config['database']['scripts']
        sql_scripts_folder = sql_scripts_config['scripts_folder']
        for key in sql_scripts_config:
            if key != 'scripts_folder':
                sql_scripts_path = sql_scripts_config[key]
                sql_scripts_config[key] = os.path.join(
                    sql_scripts_folder,
                    sql_scripts_path
                )
        return self.__create_config_object(sql_scripts_config)

    def get_app_database_config(self) -> Dict:
        full_config = self.__load_config()
        db_url = full_config['database']['connection']['app']
        echo = full_config['database']['connection']['echo']
        config = {
            "ECHO": echo,
            "DB_URL": db_url
        }
        return self.__create_config_object(config)

    def get_local_database_config(self) -> Dict:
        full_config = self.__load_config()
        db_url = full_config['database']['connection']['local']
        echo = full_config['database']['connection']['echo']
        config = {
            "ECHO": echo,
            "DB_URL": db_url
        }
        return self.__create_config_object(config)

    def get_global_config(self):
        full_config = self.__load_config()
        global_config = full_config['global']
        return ConfigObject(global_config)

    def __create_config_object(self, props: Dict):
        global_config = self.get_global_config()
        global_config.merge(props)
        return global_config

    def __load_config(self):
        with open(self._config_filepath) as f:
            data = yaml.load(f, Loader=SafeLoader)
            return data
