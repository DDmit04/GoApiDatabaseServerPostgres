from App.controller.dto.DatabaseInfoDto import DatabaseInfoDto
from App.controller.dto.DatabaseStatsDto import DatabaseStatsDto
from proto.common.Common_pb2 import ResponseResult, SendQueryResponse
from proto.server.DatabaseServerApi_pb2_grpc import DatabaseServerServiceServicer
from proto.server.DatabaseServerApi_pb2 import DatabaseOnServerResponse
from proto.common.Common_pb2 import DatabaseStatsResponse
from google.protobuf.struct_pb2 import Struct


class DatabaseController(DatabaseServerServiceServicer):

    def __init__(self, database_service, session_factory) -> None:
        super().__init__()
        self.database_service = database_service
        self.session_factory = session_factory

    def SendQuery(self, request, context):
        dbId = request.dbId
        query = request.query
        result = self.database_service.exec_user_query(self.session_factory, dbId, query)
        res = Struct()
        data = []
        for row in result:
            rowStruct = Struct()
            for key, value in row.items():
                rowStruct.update({str(key): value})
            data.append(rowStruct)
        res.update({
            "data": data
        })
        return SendQueryResponse(data=res)

    def CreateDatabase(self, request, context) -> DatabaseOnServerResponse:
        password = request.password
        db_id = request.dbId
        max_size = request.size
        res: DatabaseInfoDto = self.database_service.create_user_database(self.session_factory,
                                                                          password, max_size, db_id)
        return DatabaseOnServerResponse(username=res.username, databaseName=res.database_name)

    def DropDatabase(self, request, context):
        result = self.database_service.drop_db(self.session_factory, request.dbId)
        return ResponseResult(result=result)

    def ResetDatabase(self, request, context):
        password = request.newPassword
        db_id = request.dbId
        res: DatabaseInfoDto = self.database_service.reset_database(self.session_factory, db_id, password)
        return DatabaseOnServerResponse(username=res.username, databaseName=res.database_name)

    def UpdateDatabasePassword(self, request, context):
        newPassword = request.newPassword
        db_id = request.dbId
        result = self.database_service.update_database_password(self.session_factory, db_id, newPassword)
        return ResponseResult(result=result)

    def UpdateDatabaseSize(self, request, context):
        db_id = request.dbId
        max_size = request.newDatabaseSize
        result = self.database_service.update_database_size(self.session_factory, db_id, max_size)
        return ResponseResult(result=result)

    def GetDatabaseStats(self, request, context):
        db_id = request.dbId
        db_info: DatabaseStatsDto = self.database_service.get_target_database_stats(self.session_factory, db_id)
        return DatabaseStatsResponse(currentSize=db_info.current_size, fillPercent=db_info.fill_percent)
