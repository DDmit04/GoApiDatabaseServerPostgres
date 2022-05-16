import os.path

current_dir_path = os.path.dirname(os.path.abspath(__file__))

sql_scripts_paths = {
    "CREATE_USER_SCRIPT_PATH": os.path.join(current_dir_path, 'sqlScripts/createUser.sql'),
    "TARGET_INIT_DB_SCRIPT_PATH": os.path.join(current_dir_path, 'sqlScripts/initUserDb.sql'),
    "TARGET_UPDATE_USER_PASSWORD_SCRIPT_PATH": os.path.join(current_dir_path, 'sqlScripts/updateUserPassword.sql'),
    "TARGET_CREATE_DB_TRIGGERS_SCRIPT_PATH": os.path.join(current_dir_path,
                                                          'sqlScripts/createTriggers.sql')
}

db_config = {
    "DB_TYPE": 'postgresql',
    "DB_USERNAME": 'postgres',
    "DB_PASSWORD": 'ps',
    "DB_NAME": 'test',
    "DB_HOST": 'localhost',
    "DB_NAME_LENGTH": 5,
    "DB_USERNAME_LENGTH": 5
}

server_config = {
    "SELF_GRPC_PORT": "9091",
    "SELF_URL": "localhost",
    "DISCOVER_SERVER_URL": "localhost",
    "DISCOVER_SERVER_PORT": "9090",
    "STOPPING_SERVER_WAIT_SECONDS": 3
}
