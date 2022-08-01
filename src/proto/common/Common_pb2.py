# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Common.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x43ommon.proto\x12\ncom.common\x1a\x1cgoogle/protobuf/struct.proto\" \n\x0eResponseResult\x12\x0e\n\x06result\x18\x01 \x01(\x08\"!\n\x11\x44\x61tabaseIdRequest\x12\x0c\n\x04\x64\x62Id\x18\x01 \x01(\x05\">\n\x19\x44\x61tabaseIdPasswordRequest\x12\x0c\n\x04\x64\x62Id\x18\x01 \x01(\x05\x12\x13\n\x0bnewPassword\x18\x02 \x01(\t\"B\n\x19UpdateDatabaseSizeRequest\x12\x0c\n\x04\x64\x62Id\x18\x01 \x01(\x05\x12\x17\n\x0fnewDatabaseSize\x18\x02 \x01(\x03\":\n\x11SendQueryResponse\x12%\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"/\n\x10SendQueryRequest\x12\x0c\n\x04\x64\x62Id\x18\x01 \x01(\x05\x12\r\n\x05query\x18\x02 \x01(\t\"@\n!DatabaseIdConnectionsAllowRequest\x12\x0c\n\x04\x64\x62Id\x18\x01 \x01(\x05\x12\r\n\x05\x61llow\x18\x02 \x01(\x08\"\x07\n\x05\x45mptyB\x02P\x01\x62\x06proto3')



_RESPONSERESULT = DESCRIPTOR.message_types_by_name['ResponseResult']
_DATABASEIDREQUEST = DESCRIPTOR.message_types_by_name['DatabaseIdRequest']
_DATABASEIDPASSWORDREQUEST = DESCRIPTOR.message_types_by_name['DatabaseIdPasswordRequest']
_UPDATEDATABASESIZEREQUEST = DESCRIPTOR.message_types_by_name['UpdateDatabaseSizeRequest']
_SENDQUERYRESPONSE = DESCRIPTOR.message_types_by_name['SendQueryResponse']
_SENDQUERYREQUEST = DESCRIPTOR.message_types_by_name['SendQueryRequest']
_DATABASEIDCONNECTIONSALLOWREQUEST = DESCRIPTOR.message_types_by_name['DatabaseIdConnectionsAllowRequest']
_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
ResponseResult = _reflection.GeneratedProtocolMessageType('ResponseResult', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSERESULT,
  '__module__' : 'Common_pb2'
  # @@protoc_insertion_point(class_scope:com.common.ResponseResult)
  })
_sym_db.RegisterMessage(ResponseResult)

DatabaseIdRequest = _reflection.GeneratedProtocolMessageType('DatabaseIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _DATABASEIDREQUEST,
  '__module__' : 'Common_pb2'
  # @@protoc_insertion_point(class_scope:com.common.DatabaseIdRequest)
  })
_sym_db.RegisterMessage(DatabaseIdRequest)

DatabaseIdPasswordRequest = _reflection.GeneratedProtocolMessageType('DatabaseIdPasswordRequest', (_message.Message,), {
  'DESCRIPTOR' : _DATABASEIDPASSWORDREQUEST,
  '__module__' : 'Common_pb2'
  # @@protoc_insertion_point(class_scope:com.common.DatabaseIdPasswordRequest)
  })
_sym_db.RegisterMessage(DatabaseIdPasswordRequest)

UpdateDatabaseSizeRequest = _reflection.GeneratedProtocolMessageType('UpdateDatabaseSizeRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEDATABASESIZEREQUEST,
  '__module__' : 'Common_pb2'
  # @@protoc_insertion_point(class_scope:com.common.UpdateDatabaseSizeRequest)
  })
_sym_db.RegisterMessage(UpdateDatabaseSizeRequest)

SendQueryResponse = _reflection.GeneratedProtocolMessageType('SendQueryResponse', (_message.Message,), {
  'DESCRIPTOR' : _SENDQUERYRESPONSE,
  '__module__' : 'Common_pb2'
  # @@protoc_insertion_point(class_scope:com.common.SendQueryResponse)
  })
_sym_db.RegisterMessage(SendQueryResponse)

SendQueryRequest = _reflection.GeneratedProtocolMessageType('SendQueryRequest', (_message.Message,), {
  'DESCRIPTOR' : _SENDQUERYREQUEST,
  '__module__' : 'Common_pb2'
  # @@protoc_insertion_point(class_scope:com.common.SendQueryRequest)
  })
_sym_db.RegisterMessage(SendQueryRequest)

DatabaseIdConnectionsAllowRequest = _reflection.GeneratedProtocolMessageType('DatabaseIdConnectionsAllowRequest', (_message.Message,), {
  'DESCRIPTOR' : _DATABASEIDCONNECTIONSALLOWREQUEST,
  '__module__' : 'Common_pb2'
  # @@protoc_insertion_point(class_scope:com.common.DatabaseIdConnectionsAllowRequest)
  })
_sym_db.RegisterMessage(DatabaseIdConnectionsAllowRequest)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'Common_pb2'
  # @@protoc_insertion_point(class_scope:com.common.Empty)
  })
_sym_db.RegisterMessage(Empty)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'P\001'
  _RESPONSERESULT._serialized_start=58
  _RESPONSERESULT._serialized_end=90
  _DATABASEIDREQUEST._serialized_start=92
  _DATABASEIDREQUEST._serialized_end=125
  _DATABASEIDPASSWORDREQUEST._serialized_start=127
  _DATABASEIDPASSWORDREQUEST._serialized_end=189
  _UPDATEDATABASESIZEREQUEST._serialized_start=191
  _UPDATEDATABASESIZEREQUEST._serialized_end=257
  _SENDQUERYRESPONSE._serialized_start=259
  _SENDQUERYRESPONSE._serialized_end=317
  _SENDQUERYREQUEST._serialized_start=319
  _SENDQUERYREQUEST._serialized_end=366
  _DATABASEIDCONNECTIONSALLOWREQUEST._serialized_start=368
  _DATABASEIDCONNECTIONSALLOWREQUEST._serialized_end=432
  _EMPTY._serialized_start=434
  _EMPTY._serialized_end=441
# @@protoc_insertion_point(module_scope)