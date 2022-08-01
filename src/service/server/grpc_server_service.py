from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection
from grpc_health.v1 import health, health_pb2, health_pb2_grpc

from my_types.config_object import ConfigObject
from proto.server import DatabaseServerApi_pb2_grpc, DatabaseServerApi_pb2


class GrpcServerService:

    def __init__(self, server_config: ConfigObject):
        super().__init__()
        self.server_config = server_config

    def start_server(self, db_controller) -> grpc.Server:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        DatabaseServerApi_pb2_grpc.add_DatabaseServerServiceServicer_to_server(
            db_controller, server)
        health_servicer = health.HealthServicer()
        grpc_service_name = self.server_config.get('server_service_name')
        health_servicer.set(
            grpc_service_name,
            health_pb2.HealthCheckResponse.SERVING
        )
        health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
        server_port = self.server_config.get("self_grpc_port")

        is_dev_mode = self.server_config.get('is_dev_mode')
        if is_dev_mode:
            SERVICE_NAMES = (
                DatabaseServerApi_pb2.DESCRIPTOR
                .services_by_name['DatabaseServerService'].full_name,
                health_pb2.DESCRIPTOR
                .services_by_name['server_service_name'].full_name,
                reflection.SERVICE_NAME,
            )
            reflection.enable_server_reflection(SERVICE_NAMES, server)

        server.add_insecure_port(f'[::]:{server_port}')
        server.start()
        print(f"Start GRPC server on port {server_port}")
        return server

    def stop_server(self, grpc_server_instance):
        server_stop_delay = self.server_config \
            .get('stopping_server_wait_seconds')
        grpc_server_instance.stop(server_stop_delay)
