import grpc

from my_types.config_object import ConfigObject
from proto.register.DatabaseServerRegisterApi_pb2 import \
    DatabaseServerRegisterRequest, DatabaseInfo, \
    DatabaseServerUnregisterRequest
from proto.register.DatabaseServerRegisterApi_pb2_grpc import \
    DatabaseServerRegisterServiceStub
from service.app_database_service import AppDatabaseService
from model.database_table import Database


class ServerRegisterService:

    def __init__(self,
                 app_database_service: AppDatabaseService,
                 server_config: ConfigObject,
                 db_type: str):
        super().__init__()
        self.app_database_service = app_database_service
        self.server_config = server_config
        self.db_type = db_type

    def register(self):
        databases_info: list[Database] = self.app_database_service \
            .get_all_databases_info()
        databases_info = list(
            map(self.__database_to_request_database_info, databases_info)
        )
        stub = self.__create_grpc_stub()
        register_request = self.__create_register_request(databases_info)
        response = stub.RegisterServer(register_request)
        if not response.result:
            raise "Server fail registration!"
        else:
            print("Server registered!")

    def unregister(self):
        stub = self.__create_grpc_stub()
        self_url = self.server_config.get('self_url')
        unregister_request = DatabaseServerUnregisterRequest(
            dbUrl=self_url
        )
        stub.UnregisterServer(unregister_request)
        print("Server unregistered!")

    def __create_register_request(self, databases_info):
        self_grpc_url = self.server_config.get('self_url')
        self_grpc_port = self.server_config.get('self_grpc_port')
        self_grpc_url = f"{self_grpc_url}:{self_grpc_port}"
        disk_space = 1000
            # psutil.disk_usage('/').free
        register_request = DatabaseServerRegisterRequest(
            dbGrpcUrl=self_grpc_url,
            dbUrl=self_grpc_url,
            databaseType=self.db_type.upper(),
            freeSpace=disk_space,
            databases=databases_info
        )
        return register_request

    def __create_grpc_stub(self):
        discover_server_url = self.server_config.get('discover_server_url')
        discover_server_port = self.server_config.get('discover_server_port')
        grpc_server_url = f"{discover_server_url}:{discover_server_port}"
        register_channel = grpc.insecure_channel(grpc_server_url)
        stub = DatabaseServerRegisterServiceStub(register_channel)
        return stub

    def __database_to_request_database_info(self, database: Database):
        res = DatabaseInfo(
            dbId=database.real_db_id,
            name=database.name,
            size=database.db_size
        )
        return res
