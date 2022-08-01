from typing import Dict

from google.protobuf.struct_pb2 import Struct

from controller.dto.database_stats_dto import DatabaseStatsDto
from injector.di.dependency_container import di_container
from proto.common.Common_pb2 import ResponseResult, SendQueryResponse, \
    SendQueryRequest, DatabaseIdPasswordRequest, \
    UpdateDatabaseSizeRequest, DatabaseIdRequest, \
    DatabaseIdConnectionsAllowRequest
from proto.server.DatabaseServerApi_pb2 import CreateDatabaseOnServerRequest, \
    DatabaseStatsOnServerResponse
from proto.server.DatabaseServerApi_pb2_grpc import \
    DatabaseServerServiceServicer
from utils.controller_utils import require_app_database_session


class DatabaseController(DatabaseServerServiceServicer):

    @require_app_database_session
    def SendQuery(self,
                  session_id: str,
                  request: SendQueryRequest,
                  context) -> SendQueryResponse:
        database_service_facade = di_container\
            .get_database_service_facade(session_id)
        dbId: int = request.dbId
        query: str = request.query
        result: list[Dict] = database_service_facade\
            .exec_user_query(dbId, query)
        res: Struct = Struct()
        data: list[Struct] = []
        for row in result:
            rowStruct: Struct = Struct()
            for key, value in row.items():
                rowStruct.update({str(key): value})
            data.append(rowStruct)
        res.update({"data": data})
        return SendQueryResponse(data=res)

    @require_app_database_session
    def CreateDatabase(self,
                       session_id: str,
                       request: CreateDatabaseOnServerRequest,
                       context) -> DatabaseStatsOnServerResponse:
        database_service_facade = di_container \
            .get_database_service_facade(session_id)
        password: str = request.password
        db_id: int = request.dbId
        max_size: int = request.size
        res = database_service_facade \
            .create_user_database(db_id, password, max_size)
        return DatabaseStatsOnServerResponse(
            currentSize=res.current_size,
            fillPercent=res.fill_percent,
            databaseAndUsername=res.database_and_username,
            allowConnections=res.allow_connections
        )

    @require_app_database_session
    def DropDatabase(self,
                     session_id: str,
                     request: DatabaseIdRequest,
                     context) -> ResponseResult:
        database_service_facade = di_container \
            .get_database_service_facade(session_id)
        db_id: int = request.dbId
        result = database_service_facade.drop_database(db_id)
        return ResponseResult(result=result)

    @require_app_database_session
    def ResetDatabase(self,
                      session_id: str,
                      request: DatabaseIdPasswordRequest,
                      context) -> DatabaseStatsOnServerResponse:
        database_service_facade = di_container \
            .get_database_service_facade(session_id)
        password: str = request.newPassword
        db_id: int = request.dbId
        res = database_service_facade.reset_database(db_id, password)
        return DatabaseStatsOnServerResponse(
            currentSize=res.current_size,
            fillPercent=res.fill_percent,
            databaseAndUsername=res.database_and_username,
            allowConnections=res.allow_connections
        )

    @require_app_database_session
    def UpdateDatabasePassword(self,
                               session_id: str,
                               request: DatabaseIdPasswordRequest,
                               context) -> ResponseResult:
        database_service_facade = di_container \
            .get_database_service_facade(session_id)
        newPassword: str = request.newPassword
        db_id: int = request.dbId
        result: bool = database_service_facade.update_database_password(
            db_id, newPassword
        )
        return ResponseResult(result=result)

    @require_app_database_session
    def UpdateDatabaseSize(self,
                           session_id: str,
                           request: UpdateDatabaseSizeRequest,
                           context) -> ResponseResult:
        database_service_facade = di_container \
            .get_database_service_facade(session_id)
        db_id: int = request.dbId
        max_size: int = request.newDatabaseSize
        result: bool = database_service_facade.update_database_size(
            db_id, max_size
        )
        return ResponseResult(result=result)

    @require_app_database_session
    def GetDatabaseStats(self,
                         session_id: str,
                         request: DatabaseIdRequest,
                         context) -> DatabaseStatsOnServerResponse:
        database_service_facade = di_container \
            .get_database_service_facade(session_id)
        db_id: int = request.dbId
        db_info: DatabaseStatsDto = database_service_facade\
            .get_database_stats(db_id)
        return DatabaseStatsOnServerResponse(
            currentSize=db_info.current_size,
            fillPercent=db_info.fill_percent,
            databaseAndUsername=db_info.database_and_username,
            allowConnections=db_info.allow_connections
        )

    @require_app_database_session
    def UpdateDatabaseAllowConnections(self,
                                       session_id: str,
                                       request: DatabaseIdConnectionsAllowRequest,
                                       context) -> ResponseResult:
        database_service_facade = di_container \
            .get_database_service_facade(session_id)
        db_id: int = request.dbId
        allow: bool = request.allow
        result = database_service_facade.change_allow_connections(
            db_id, allow
        )
        return ResponseResult(result=result)
