import atexit
from concurrent import futures

import grpc
from grpc_health.v1 import health_pb2_grpc, health, health_pb2

import Config
from App.utils.DataUtils import database_info_to_request_database_info
from App.utils.DbConnectionUtils import get_db_session_factory, get_db_engine
from App.controller.DatabaseControllerGrpc import DatabaseController
from App.controller.DeviceControllerGrpc import DeviceControllerGrpc
from proto.register.DatabaseServerRegisterApi_pb2 import DatabaseServerUnregisterRequest, DatabaseServerRegisterRequest
from proto.register.DatabaseServerRegisterApi_pb2_grpc import DatabaseServerRegisterServiceStub
from proto.server import DatabaseServerApi_pb2_grpc
from App.repo.LocalDatabaseRepo import LocalDatabaseRepository
from App.repo.TargetDatabaseRepo import TargetDatabaseRepository
from App.service.DatabaseService import DatabaseService
from App.service.DeviceService import ServerService

grpc_server_instance = None


def start_grpc_server(db_controller, device_stats_controller):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    DatabaseServerApi_pb2_grpc.add_DatabaseServerServiceServicer_to_server(db_controller, server)
    DatabaseServerApi_pb2_grpc.add_DatabaseServerStatsServiceServicer_to_server(device_stats_controller, server)
    health_servicer = health.HealthServicer()
    health_servicer.set("DatabaseServerService", health_pb2.HealthCheckResponse.SERVING)
    health_servicer.set("DatabaseServerStatsService", health_pb2.HealthCheckResponse.SERVING)
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    server.add_insecure_port(f'[::]:{Config.server_config["SELF_GRPC_PORT"]}')
    server.start()
    print(f"Start GRPC server on port {Config.server_config['SELF_GRPC_PORT']}")
    return server


def create_session_factory():
    db_engine = get_db_engine(Config.db_config)
    factory = get_db_session_factory(db_engine)
    return factory


def register_self():
    databases_info = database_service.get_local_databases_info(session_factory)
    databases_info = list(map(database_info_to_request_database_info, databases_info))
    grpc_server_url = f"{Config.server_config['DISCOVER_SERVER_URL']}:{Config.server_config['DISCOVER_SERVER_PORT']}"
    register_channel = grpc.insecure_channel(grpc_server_url)
    stub = DatabaseServerRegisterServiceStub(register_channel)
    self_grpc_url = f"{Config.server_config['SELF_URL']}:{Config.server_config['SELF_GRPC_PORT']}"
    register_request = DatabaseServerRegisterRequest(
        dbGrpcUrl=self_grpc_url,
        dbUrl=Config.server_config['SELF_URL'],
        databaseType=Config.db_config['DB_TYPE'].upper(),
        freeSpace=server_service.get_free_disk_space(),
        databases=databases_info)
    response = stub.RegisterServer(register_request)
    if not response.result:
        raise "Server fail registration!"
    else:
        print("Server registered!")


def on_app_close():
    try:
        grpc_server_instance.stop(Config.server_config['STOPPING_SERVER_WAIT_SECONDS'])
    finally:
        grpc_server_url = f"{Config.server_config['DISCOVER_SERVER_URL']}:{Config.server_config['DISCOVER_SERVER_PORT']}"
        unregister_channel = grpc.insecure_channel(grpc_server_url)
        client = DatabaseServerRegisterServiceStub(unregister_channel)
        unregister_request = DatabaseServerUnregisterRequest(dbUrl=Config.server_config['SELF_URL'])
        client.UnregisterServer(unregister_request)
        print("Server unregistered!")


if __name__ == '__main__':
    session_factory = create_session_factory()

    local_db_repo = LocalDatabaseRepository()
    target_db_repo = TargetDatabaseRepository()

    server_service = ServerService()
    database_service = DatabaseService(local_db_repo, target_db_repo)

    database_controller = DatabaseController(database_service, session_factory)
    device_controller = DeviceControllerGrpc(server_service)

    grpc_server_instance = start_grpc_server(database_controller, device_controller)

    register_self()

    atexit.register(on_app_close)

    grpc_server_instance.wait_for_termination()
