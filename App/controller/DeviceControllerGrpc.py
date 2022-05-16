from App.controller.dto.ServerStatsDto import ServerStatDto
from proto.server.DatabaseServerApi_pb2_grpc import DatabaseServerStatsServiceServicer
from proto.common.Common_pb2 import DatabaseStatsResponse


class DeviceControllerGrpc(DatabaseServerStatsServiceServicer):

    def __init__(self, server_service) -> None:
        super().__init__()
        self.server_service = server_service

    def GetServerStats(self, request, context):
        serverStatsDto: ServerStatDto = self.server_service.get_server_stats()
        return DatabaseStatsResponse(freeSpace=serverStatsDto.free_space)
