import atexit

import grpc

from controller.database_controller_grpc import DatabaseController
from injector.di.dependency_container import di_container


def start_server() -> grpc.Server:
    database_controller = DatabaseController()
    grpc_server_service = di_container.get_grpc_server_service()
    server_instance = grpc_server_service \
        .start_server(database_controller)

    register_service = di_container.get_server_register_service("")
    register_service.register()
    di_container.close_app_database_session("")
    atexit.register(
        stop_server,
        server_instance
    )
    return server_instance


def stop_server(server_instance):
    grpc_server_service = di_container.get_grpc_server_service()
    grpc_server_service.stop_server(server_instance)
    register_service = di_container.get_server_register_service("")
    register_service.unregister()
    di_container.close_app_database_session("")


if __name__ == '__main__':
    grpc_server_instance = start_server()
    grpc_server_instance.wait_for_termination()
