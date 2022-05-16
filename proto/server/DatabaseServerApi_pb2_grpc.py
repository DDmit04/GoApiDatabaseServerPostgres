# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import proto.common.Common_pb2 as Common__pb2
import proto.server.DatabaseServerApi_pb2 as DatabaseServerApi__pb2


class DatabaseServerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateDatabase = channel.unary_unary(
                '/com.server.DatabaseServerService/CreateDatabase',
                request_serializer=DatabaseServerApi__pb2.CreateDatabaseOnServerRequest.SerializeToString,
                response_deserializer=DatabaseServerApi__pb2.DatabaseOnServerResponse.FromString,
                )
        self.DropDatabase = channel.unary_unary(
                '/com.server.DatabaseServerService/DropDatabase',
                request_serializer=Common__pb2.DatabaseIdRequest.SerializeToString,
                response_deserializer=Common__pb2.ResponseResult.FromString,
                )
        self.ResetDatabase = channel.unary_unary(
                '/com.server.DatabaseServerService/ResetDatabase',
                request_serializer=Common__pb2.ResetDatabaseRequest.SerializeToString,
                response_deserializer=DatabaseServerApi__pb2.DatabaseOnServerResponse.FromString,
                )
        self.UpdateDatabasePassword = channel.unary_unary(
                '/com.server.DatabaseServerService/UpdateDatabasePassword',
                request_serializer=Common__pb2.UpdateDatabasePasswordRequest.SerializeToString,
                response_deserializer=Common__pb2.ResponseResult.FromString,
                )
        self.UpdateDatabaseSize = channel.unary_unary(
                '/com.server.DatabaseServerService/UpdateDatabaseSize',
                request_serializer=Common__pb2.UpdateDatabaseSizeRequest.SerializeToString,
                response_deserializer=Common__pb2.ResponseResult.FromString,
                )
        self.GetDatabaseStats = channel.unary_unary(
                '/com.server.DatabaseServerService/GetDatabaseStats',
                request_serializer=Common__pb2.DatabaseIdRequest.SerializeToString,
                response_deserializer=Common__pb2.DatabaseStatsResponse.FromString,
                )
        self.SendQuery = channel.unary_unary(
                '/com.server.DatabaseServerService/SendQuery',
                request_serializer=Common__pb2.SendQueryRequest.SerializeToString,
                response_deserializer=Common__pb2.SendQueryResponse.FromString,
                )


class DatabaseServerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateDatabase(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DropDatabase(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ResetDatabase(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDatabasePassword(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDatabaseSize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDatabaseStats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendQuery(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DatabaseServerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateDatabase': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateDatabase,
                    request_deserializer=DatabaseServerApi__pb2.CreateDatabaseOnServerRequest.FromString,
                    response_serializer=DatabaseServerApi__pb2.DatabaseOnServerResponse.SerializeToString,
            ),
            'DropDatabase': grpc.unary_unary_rpc_method_handler(
                    servicer.DropDatabase,
                    request_deserializer=Common__pb2.DatabaseIdRequest.FromString,
                    response_serializer=Common__pb2.ResponseResult.SerializeToString,
            ),
            'ResetDatabase': grpc.unary_unary_rpc_method_handler(
                    servicer.ResetDatabase,
                    request_deserializer=Common__pb2.ResetDatabaseRequest.FromString,
                    response_serializer=DatabaseServerApi__pb2.DatabaseOnServerResponse.SerializeToString,
            ),
            'UpdateDatabasePassword': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateDatabasePassword,
                    request_deserializer=Common__pb2.UpdateDatabasePasswordRequest.FromString,
                    response_serializer=Common__pb2.ResponseResult.SerializeToString,
            ),
            'UpdateDatabaseSize': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateDatabaseSize,
                    request_deserializer=Common__pb2.UpdateDatabaseSizeRequest.FromString,
                    response_serializer=Common__pb2.ResponseResult.SerializeToString,
            ),
            'GetDatabaseStats': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDatabaseStats,
                    request_deserializer=Common__pb2.DatabaseIdRequest.FromString,
                    response_serializer=Common__pb2.DatabaseStatsResponse.SerializeToString,
            ),
            'SendQuery': grpc.unary_unary_rpc_method_handler(
                    servicer.SendQuery,
                    request_deserializer=Common__pb2.SendQueryRequest.FromString,
                    response_serializer=Common__pb2.SendQueryResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.server.DatabaseServerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DatabaseServerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateDatabase(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.server.DatabaseServerService/CreateDatabase',
            DatabaseServerApi__pb2.CreateDatabaseOnServerRequest.SerializeToString,
            DatabaseServerApi__pb2.DatabaseOnServerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DropDatabase(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.server.DatabaseServerService/DropDatabase',
            Common__pb2.DatabaseIdRequest.SerializeToString,
            Common__pb2.ResponseResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ResetDatabase(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.server.DatabaseServerService/ResetDatabase',
            Common__pb2.ResetDatabaseRequest.SerializeToString,
            DatabaseServerApi__pb2.DatabaseOnServerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateDatabasePassword(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.server.DatabaseServerService/UpdateDatabasePassword',
            Common__pb2.UpdateDatabasePasswordRequest.SerializeToString,
            Common__pb2.ResponseResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateDatabaseSize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.server.DatabaseServerService/UpdateDatabaseSize',
            Common__pb2.UpdateDatabaseSizeRequest.SerializeToString,
            Common__pb2.ResponseResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDatabaseStats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.server.DatabaseServerService/GetDatabaseStats',
            Common__pb2.DatabaseIdRequest.SerializeToString,
            Common__pb2.DatabaseStatsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendQuery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.server.DatabaseServerService/SendQuery',
            Common__pb2.SendQueryRequest.SerializeToString,
            Common__pb2.SendQueryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class DatabaseServerStatsServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetServerStats = channel.unary_unary(
                '/com.server.DatabaseServerStatsService/GetServerStats',
                request_serializer=Common__pb2.DatabaseIdRequest.SerializeToString,
                response_deserializer=Common__pb2.DatabaseStatsResponse.FromString,
                )


class DatabaseServerStatsServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetServerStats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DatabaseServerStatsServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetServerStats': grpc.unary_unary_rpc_method_handler(
                    servicer.GetServerStats,
                    request_deserializer=Common__pb2.DatabaseIdRequest.FromString,
                    response_serializer=Common__pb2.DatabaseStatsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.server.DatabaseServerStatsService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DatabaseServerStatsService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetServerStats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.server.DatabaseServerStatsService/GetServerStats',
            Common__pb2.DatabaseIdRequest.SerializeToString,
            Common__pb2.DatabaseStatsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
