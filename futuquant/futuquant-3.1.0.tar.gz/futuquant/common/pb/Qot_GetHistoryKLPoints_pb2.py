# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Qot_GetHistoryKLPoints.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import Common_pb2 as Common__pb2
import Qot_Common_pb2 as Qot__Common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='Qot_GetHistoryKLPoints.proto',
  package='Qot_GetHistoryKLPoints',
  syntax='proto2',
  serialized_pb=_b('\n\x1cQot_GetHistoryKLPoints.proto\x12\x16Qot_GetHistoryKLPoints\x1a\x0c\x43ommon.proto\x1a\x10Qot_Common.proto\"\xaf\x01\n\x03\x43\x32S\x12\x11\n\trehabType\x18\x01 \x02(\x05\x12\x0e\n\x06klType\x18\x02 \x02(\x05\x12\x12\n\nnoDataMode\x18\x03 \x02(\x05\x12*\n\x0csecurityList\x18\x04 \x03(\x0b\x32\x14.Qot_Common.Security\x12\x10\n\x08timeList\x18\x05 \x03(\t\x12\x19\n\x11maxReqSecurityNum\x18\x06 \x01(\x05\x12\x18\n\x10needKLFieldsFlag\x18\x07 \x01(\x03\"Q\n\x0fHistoryPointsKL\x12\x0e\n\x06status\x18\x01 \x02(\x05\x12\x0f\n\x07reqTime\x18\x02 \x02(\t\x12\x1d\n\x02kl\x18\x03 \x02(\x0b\x32\x11.Qot_Common.KLine\"z\n\x17SecurityHistoryKLPoints\x12&\n\x08security\x18\x01 \x02(\x0b\x32\x14.Qot_Common.Security\x12\x37\n\x06klList\x18\x02 \x03(\x0b\x32\'.Qot_GetHistoryKLPoints.HistoryPointsKL\"\\\n\x03S2C\x12\x44\n\x0bklPointList\x18\x01 \x03(\x0b\x32/.Qot_GetHistoryKLPoints.SecurityHistoryKLPoints\x12\x0f\n\x07hasNext\x18\x02 \x01(\x08\"3\n\x07Request\x12(\n\x03\x63\x32s\x18\x01 \x02(\x0b\x32\x1b.Qot_GetHistoryKLPoints.C2S\"l\n\x08Response\x12\x15\n\x07retType\x18\x01 \x02(\x05:\x04-400\x12\x0e\n\x06retMsg\x18\x02 \x01(\t\x12\x0f\n\x07\x65rrCode\x18\x03 \x01(\x05\x12(\n\x03s2c\x18\x04 \x01(\x0b\x32\x1b.Qot_GetHistoryKLPoints.S2C*R\n\nNoDataMode\x12\x13\n\x0fNoDataMode_Null\x10\x00\x12\x16\n\x12NoDataMode_Forward\x10\x01\x12\x17\n\x13NoDataMode_Backward\x10\x02*g\n\nDataStatus\x12\x13\n\x0f\x44\x61taStatus_Null\x10\x00\x12\x16\n\x12\x44\x61taStatus_Current\x10\x01\x12\x17\n\x13\x44\x61taStatus_Previous\x10\x02\x12\x13\n\x0f\x44\x61taStatus_Back\x10\x03')
  ,
  dependencies=[Common__pb2.DESCRIPTOR,Qot__Common__pb2.DESCRIPTOR,])

_NODATAMODE = _descriptor.EnumDescriptor(
  name='NoDataMode',
  full_name='Qot_GetHistoryKLPoints.NoDataMode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NoDataMode_Null', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NoDataMode_Forward', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NoDataMode_Backward', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=730,
  serialized_end=812,
)
_sym_db.RegisterEnumDescriptor(_NODATAMODE)

NoDataMode = enum_type_wrapper.EnumTypeWrapper(_NODATAMODE)
_DATASTATUS = _descriptor.EnumDescriptor(
  name='DataStatus',
  full_name='Qot_GetHistoryKLPoints.DataStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DataStatus_Null', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DataStatus_Current', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DataStatus_Previous', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DataStatus_Back', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=814,
  serialized_end=917,
)
_sym_db.RegisterEnumDescriptor(_DATASTATUS)

DataStatus = enum_type_wrapper.EnumTypeWrapper(_DATASTATUS)
NoDataMode_Null = 0
NoDataMode_Forward = 1
NoDataMode_Backward = 2
DataStatus_Null = 0
DataStatus_Current = 1
DataStatus_Previous = 2
DataStatus_Back = 3



_C2S = _descriptor.Descriptor(
  name='C2S',
  full_name='Qot_GetHistoryKLPoints.C2S',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rehabType', full_name='Qot_GetHistoryKLPoints.C2S.rehabType', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='klType', full_name='Qot_GetHistoryKLPoints.C2S.klType', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='noDataMode', full_name='Qot_GetHistoryKLPoints.C2S.noDataMode', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='securityList', full_name='Qot_GetHistoryKLPoints.C2S.securityList', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeList', full_name='Qot_GetHistoryKLPoints.C2S.timeList', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='maxReqSecurityNum', full_name='Qot_GetHistoryKLPoints.C2S.maxReqSecurityNum', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='needKLFieldsFlag', full_name='Qot_GetHistoryKLPoints.C2S.needKLFieldsFlag', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=89,
  serialized_end=264,
)


_HISTORYPOINTSKL = _descriptor.Descriptor(
  name='HistoryPointsKL',
  full_name='Qot_GetHistoryKLPoints.HistoryPointsKL',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='Qot_GetHistoryKLPoints.HistoryPointsKL.status', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reqTime', full_name='Qot_GetHistoryKLPoints.HistoryPointsKL.reqTime', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='kl', full_name='Qot_GetHistoryKLPoints.HistoryPointsKL.kl', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=266,
  serialized_end=347,
)


_SECURITYHISTORYKLPOINTS = _descriptor.Descriptor(
  name='SecurityHistoryKLPoints',
  full_name='Qot_GetHistoryKLPoints.SecurityHistoryKLPoints',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='security', full_name='Qot_GetHistoryKLPoints.SecurityHistoryKLPoints.security', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='klList', full_name='Qot_GetHistoryKLPoints.SecurityHistoryKLPoints.klList', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=349,
  serialized_end=471,
)


_S2C = _descriptor.Descriptor(
  name='S2C',
  full_name='Qot_GetHistoryKLPoints.S2C',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='klPointList', full_name='Qot_GetHistoryKLPoints.S2C.klPointList', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hasNext', full_name='Qot_GetHistoryKLPoints.S2C.hasNext', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=473,
  serialized_end=565,
)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='Qot_GetHistoryKLPoints.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='c2s', full_name='Qot_GetHistoryKLPoints.Request.c2s', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=567,
  serialized_end=618,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='Qot_GetHistoryKLPoints.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='retType', full_name='Qot_GetHistoryKLPoints.Response.retType', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=True, default_value=-400,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='retMsg', full_name='Qot_GetHistoryKLPoints.Response.retMsg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='errCode', full_name='Qot_GetHistoryKLPoints.Response.errCode', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='s2c', full_name='Qot_GetHistoryKLPoints.Response.s2c', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=620,
  serialized_end=728,
)

_C2S.fields_by_name['securityList'].message_type = Qot__Common__pb2._SECURITY
_HISTORYPOINTSKL.fields_by_name['kl'].message_type = Qot__Common__pb2._KLINE
_SECURITYHISTORYKLPOINTS.fields_by_name['security'].message_type = Qot__Common__pb2._SECURITY
_SECURITYHISTORYKLPOINTS.fields_by_name['klList'].message_type = _HISTORYPOINTSKL
_S2C.fields_by_name['klPointList'].message_type = _SECURITYHISTORYKLPOINTS
_REQUEST.fields_by_name['c2s'].message_type = _C2S
_RESPONSE.fields_by_name['s2c'].message_type = _S2C
DESCRIPTOR.message_types_by_name['C2S'] = _C2S
DESCRIPTOR.message_types_by_name['HistoryPointsKL'] = _HISTORYPOINTSKL
DESCRIPTOR.message_types_by_name['SecurityHistoryKLPoints'] = _SECURITYHISTORYKLPOINTS
DESCRIPTOR.message_types_by_name['S2C'] = _S2C
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
DESCRIPTOR.enum_types_by_name['NoDataMode'] = _NODATAMODE
DESCRIPTOR.enum_types_by_name['DataStatus'] = _DATASTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

C2S = _reflection.GeneratedProtocolMessageType('C2S', (_message.Message,), dict(
  DESCRIPTOR = _C2S,
  __module__ = 'Qot_GetHistoryKLPoints_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetHistoryKLPoints.C2S)
  ))
_sym_db.RegisterMessage(C2S)

HistoryPointsKL = _reflection.GeneratedProtocolMessageType('HistoryPointsKL', (_message.Message,), dict(
  DESCRIPTOR = _HISTORYPOINTSKL,
  __module__ = 'Qot_GetHistoryKLPoints_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetHistoryKLPoints.HistoryPointsKL)
  ))
_sym_db.RegisterMessage(HistoryPointsKL)

SecurityHistoryKLPoints = _reflection.GeneratedProtocolMessageType('SecurityHistoryKLPoints', (_message.Message,), dict(
  DESCRIPTOR = _SECURITYHISTORYKLPOINTS,
  __module__ = 'Qot_GetHistoryKLPoints_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetHistoryKLPoints.SecurityHistoryKLPoints)
  ))
_sym_db.RegisterMessage(SecurityHistoryKLPoints)

S2C = _reflection.GeneratedProtocolMessageType('S2C', (_message.Message,), dict(
  DESCRIPTOR = _S2C,
  __module__ = 'Qot_GetHistoryKLPoints_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetHistoryKLPoints.S2C)
  ))
_sym_db.RegisterMessage(S2C)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'Qot_GetHistoryKLPoints_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetHistoryKLPoints.Request)
  ))
_sym_db.RegisterMessage(Request)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'Qot_GetHistoryKLPoints_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetHistoryKLPoints.Response)
  ))
_sym_db.RegisterMessage(Response)


# @@protoc_insertion_point(module_scope)
