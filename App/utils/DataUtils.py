from proto.register.DatabaseServerRegisterApi_pb2 import DatabaseInfo


def database_info_to_request_database_info(database_info):
    res = DatabaseInfo(
        dbId=database_info['db_id'],
        username=database_info['username'],
        dbName=database_info['db_name'],
        size=database_info['db_size']
    )
    return res
