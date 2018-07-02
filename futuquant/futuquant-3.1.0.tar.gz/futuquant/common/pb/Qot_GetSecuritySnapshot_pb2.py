# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Qot_GetSecuritySnapshot.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
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
  name='Qot_GetSecuritySnapshot.proto',
  package='Qot_GetSecuritySnapshot',
  syntax='proto2',
  serialized_pb=_b('\n\x1dQot_GetSecuritySnapshot.proto\x12\x17Qot_GetSecuritySnapshot\x1a\x0c\x43ommon.proto\x1a\x10Qot_Common.proto\"1\n\x03\x43\x32S\x12*\n\x0csecurityList\x18\x01 \x03(\x0b\x32\x14.Qot_Common.Security\"\x87\x02\n\x14\x45quitySnapshotExData\x12\x14\n\x0cissuedShares\x18\x01 \x02(\x03\x12\x17\n\x0fissuedMarketVal\x18\x02 \x02(\x01\x12\x10\n\x08netAsset\x18\x03 \x02(\x01\x12\x11\n\tnetProfit\x18\x04 \x02(\x01\x12\x18\n\x10\x65\x61rningsPershare\x18\x05 \x02(\x01\x12\x19\n\x11outstandingShares\x18\x06 \x02(\x03\x12\x1c\n\x14outstandingMarketVal\x18\x07 \x02(\x01\x12\x18\n\x10netAssetPershare\x18\x08 \x02(\x01\x12\x0e\n\x06\x65yRate\x18\t \x02(\x01\x12\x0e\n\x06peRate\x18\n \x02(\x01\x12\x0e\n\x06pbRate\x18\x0b \x02(\x01\"\xbb\x02\n\x15WarrantSnapshotExData\x12\x16\n\x0e\x63onversionRate\x18\x01 \x02(\x01\x12\x13\n\x0bwarrantType\x18\x02 \x02(\x05\x12\x13\n\x0bstrikePrice\x18\x03 \x02(\x01\x12\x14\n\x0cmaturityTime\x18\x04 \x02(\t\x12\x14\n\x0c\x65ndTradeTime\x18\x05 \x02(\t\x12#\n\x05owner\x18\x06 \x02(\x0b\x32\x14.Qot_Common.Security\x12\x15\n\rrecoveryPrice\x18\x07 \x02(\x01\x12\x14\n\x0cstreetVolumn\x18\x08 \x02(\x03\x12\x13\n\x0bissueVolumn\x18\t \x02(\x03\x12\x12\n\nstreetRate\x18\n \x02(\x01\x12\r\n\x05\x64\x65lta\x18\x0b \x02(\x01\x12\x19\n\x11impliedVolatility\x18\x0c \x02(\x01\x12\x0f\n\x07premium\x18\r \x02(\x01\"\xc2\x02\n\x11SnapshotBasicData\x12&\n\x08security\x18\x01 \x02(\x0b\x32\x14.Qot_Common.Security\x12\x0c\n\x04type\x18\x02 \x02(\x05\x12\x11\n\tisSuspend\x18\x03 \x02(\x08\x12\x10\n\x08listTime\x18\x04 \x02(\t\x12\x0f\n\x07lotSize\x18\x05 \x02(\x05\x12\x13\n\x0bpriceSpread\x18\x06 \x02(\x01\x12\x12\n\nupdateTime\x18\x07 \x02(\t\x12\x11\n\thighPrice\x18\x08 \x02(\x01\x12\x11\n\topenPrice\x18\t \x02(\x01\x12\x10\n\x08lowPrice\x18\n \x02(\x01\x12\x16\n\x0elastClosePrice\x18\x0b \x02(\x01\x12\x10\n\x08\x63urPrice\x18\x0c \x02(\x01\x12\x0e\n\x06volume\x18\r \x02(\x03\x12\x10\n\x08turnover\x18\x0e \x02(\x01\x12\x14\n\x0cturnoverRate\x18\x0f \x02(\x01\"\xd1\x01\n\x08Snapshot\x12\x39\n\x05\x62\x61sic\x18\x01 \x02(\x0b\x32*.Qot_GetSecuritySnapshot.SnapshotBasicData\x12\x43\n\x0c\x65quityExData\x18\x02 \x01(\x0b\x32-.Qot_GetSecuritySnapshot.EquitySnapshotExData\x12\x45\n\rwarrantExData\x18\x03 \x01(\x0b\x32..Qot_GetSecuritySnapshot.WarrantSnapshotExData\">\n\x03S2C\x12\x37\n\x0csnapshotList\x18\x01 \x03(\x0b\x32!.Qot_GetSecuritySnapshot.Snapshot\"4\n\x07Request\x12)\n\x03\x63\x32s\x18\x01 \x02(\x0b\x32\x1c.Qot_GetSecuritySnapshot.C2S\"m\n\x08Response\x12\x15\n\x07retType\x18\x01 \x02(\x05:\x04-400\x12\x0e\n\x06retMsg\x18\x02 \x01(\t\x12\x0f\n\x07\x65rrCode\x18\x03 \x01(\x05\x12)\n\x03s2c\x18\x04 \x01(\x0b\x32\x1c.Qot_GetSecuritySnapshot.S2C')
  ,
  dependencies=[Common__pb2.DESCRIPTOR,Qot__Common__pb2.DESCRIPTOR,])




_C2S = _descriptor.Descriptor(
  name='C2S',
  full_name='Qot_GetSecuritySnapshot.C2S',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='securityList', full_name='Qot_GetSecuritySnapshot.C2S.securityList', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=90,
  serialized_end=139,
)


_EQUITYSNAPSHOTEXDATA = _descriptor.Descriptor(
  name='EquitySnapshotExData',
  full_name='Qot_GetSecuritySnapshot.EquitySnapshotExData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='issuedShares', full_name='Qot_GetSecuritySnapshot.EquitySnapshotExData.issuedShares', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='issuedMarketVal', full_name='Qot_GetSecuritySnapshot.EquitySnapshotExData.issuedMarketVal', index=1,
      number=2, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='netAsset', full_name='Qot_GetSecuritySnapshot.EquitySnapshotExData.netAsset', index=2,
      number=3, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='netProfit', full_name='Qot_GetSecuritySnapshot.EquitySnapshotExData.netProfit', index=3,
      number=4, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='earningsPershare', full_name='Qot_GetSecuritySnapshot.EquitySnapshotExData.earningsPershare', index=4,
      number=5, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='outstandingShares', full_name='Qot_GetSecuritySnapshot.EquitySnapshotExData.outstandingShares', index=5,
      number=6, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='outstandingMarketVal', full_name='Qot_GetSecuritySnapshot.EquitySnapshotExData.outstandingMarketVal', index=6,
      number=7, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='netAssetPershare', full_name='Qot_GetSecuritySnapshot.EquitySnapshotExData.netAssetPershare', index=7,
      number=8, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eyRate', full_name='Qot_GetSecuritySnapshot.EquitySnapshotExData.eyRate', index=8,
      number=9, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='peRate', full_name='Qot_GetSecuritySnapshot.EquitySnapshotExData.peRate', index=9,
      number=10, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pbRate', full_name='Qot_GetSecuritySnapshot.EquitySnapshotExData.pbRate', index=10,
      number=11, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
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
  serialized_start=142,
  serialized_end=405,
)


_WARRANTSNAPSHOTEXDATA = _descriptor.Descriptor(
  name='WarrantSnapshotExData',
  full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='conversionRate', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.conversionRate', index=0,
      number=1, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='warrantType', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.warrantType', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='strikePrice', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.strikePrice', index=2,
      number=3, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='maturityTime', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.maturityTime', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='endTradeTime', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.endTradeTime', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='owner', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.owner', index=5,
      number=6, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='recoveryPrice', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.recoveryPrice', index=6,
      number=7, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='streetVolumn', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.streetVolumn', index=7,
      number=8, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='issueVolumn', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.issueVolumn', index=8,
      number=9, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='streetRate', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.streetRate', index=9,
      number=10, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='delta', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.delta', index=10,
      number=11, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='impliedVolatility', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.impliedVolatility', index=11,
      number=12, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='premium', full_name='Qot_GetSecuritySnapshot.WarrantSnapshotExData.premium', index=12,
      number=13, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
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
  serialized_start=408,
  serialized_end=723,
)


_SNAPSHOTBASICDATA = _descriptor.Descriptor(
  name='SnapshotBasicData',
  full_name='Qot_GetSecuritySnapshot.SnapshotBasicData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='security', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.security', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.type', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='isSuspend', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.isSuspend', index=2,
      number=3, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='listTime', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.listTime', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lotSize', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.lotSize', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='priceSpread', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.priceSpread', index=5,
      number=6, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='updateTime', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.updateTime', index=6,
      number=7, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='highPrice', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.highPrice', index=7,
      number=8, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='openPrice', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.openPrice', index=8,
      number=9, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lowPrice', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.lowPrice', index=9,
      number=10, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lastClosePrice', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.lastClosePrice', index=10,
      number=11, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='curPrice', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.curPrice', index=11,
      number=12, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='volume', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.volume', index=12,
      number=13, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='turnover', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.turnover', index=13,
      number=14, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='turnoverRate', full_name='Qot_GetSecuritySnapshot.SnapshotBasicData.turnoverRate', index=14,
      number=15, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
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
  serialized_start=726,
  serialized_end=1048,
)


_SNAPSHOT = _descriptor.Descriptor(
  name='Snapshot',
  full_name='Qot_GetSecuritySnapshot.Snapshot',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='basic', full_name='Qot_GetSecuritySnapshot.Snapshot.basic', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='equityExData', full_name='Qot_GetSecuritySnapshot.Snapshot.equityExData', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='warrantExData', full_name='Qot_GetSecuritySnapshot.Snapshot.warrantExData', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=1051,
  serialized_end=1260,
)


_S2C = _descriptor.Descriptor(
  name='S2C',
  full_name='Qot_GetSecuritySnapshot.S2C',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='snapshotList', full_name='Qot_GetSecuritySnapshot.S2C.snapshotList', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=1262,
  serialized_end=1324,
)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='Qot_GetSecuritySnapshot.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='c2s', full_name='Qot_GetSecuritySnapshot.Request.c2s', index=0,
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
  serialized_start=1326,
  serialized_end=1378,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='Qot_GetSecuritySnapshot.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='retType', full_name='Qot_GetSecuritySnapshot.Response.retType', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=True, default_value=-400,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='retMsg', full_name='Qot_GetSecuritySnapshot.Response.retMsg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='errCode', full_name='Qot_GetSecuritySnapshot.Response.errCode', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='s2c', full_name='Qot_GetSecuritySnapshot.Response.s2c', index=3,
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
  serialized_start=1380,
  serialized_end=1489,
)

_C2S.fields_by_name['securityList'].message_type = Qot__Common__pb2._SECURITY
_WARRANTSNAPSHOTEXDATA.fields_by_name['owner'].message_type = Qot__Common__pb2._SECURITY
_SNAPSHOTBASICDATA.fields_by_name['security'].message_type = Qot__Common__pb2._SECURITY
_SNAPSHOT.fields_by_name['basic'].message_type = _SNAPSHOTBASICDATA
_SNAPSHOT.fields_by_name['equityExData'].message_type = _EQUITYSNAPSHOTEXDATA
_SNAPSHOT.fields_by_name['warrantExData'].message_type = _WARRANTSNAPSHOTEXDATA
_S2C.fields_by_name['snapshotList'].message_type = _SNAPSHOT
_REQUEST.fields_by_name['c2s'].message_type = _C2S
_RESPONSE.fields_by_name['s2c'].message_type = _S2C
DESCRIPTOR.message_types_by_name['C2S'] = _C2S
DESCRIPTOR.message_types_by_name['EquitySnapshotExData'] = _EQUITYSNAPSHOTEXDATA
DESCRIPTOR.message_types_by_name['WarrantSnapshotExData'] = _WARRANTSNAPSHOTEXDATA
DESCRIPTOR.message_types_by_name['SnapshotBasicData'] = _SNAPSHOTBASICDATA
DESCRIPTOR.message_types_by_name['Snapshot'] = _SNAPSHOT
DESCRIPTOR.message_types_by_name['S2C'] = _S2C
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

C2S = _reflection.GeneratedProtocolMessageType('C2S', (_message.Message,), dict(
  DESCRIPTOR = _C2S,
  __module__ = 'Qot_GetSecuritySnapshot_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetSecuritySnapshot.C2S)
  ))
_sym_db.RegisterMessage(C2S)

EquitySnapshotExData = _reflection.GeneratedProtocolMessageType('EquitySnapshotExData', (_message.Message,), dict(
  DESCRIPTOR = _EQUITYSNAPSHOTEXDATA,
  __module__ = 'Qot_GetSecuritySnapshot_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetSecuritySnapshot.EquitySnapshotExData)
  ))
_sym_db.RegisterMessage(EquitySnapshotExData)

WarrantSnapshotExData = _reflection.GeneratedProtocolMessageType('WarrantSnapshotExData', (_message.Message,), dict(
  DESCRIPTOR = _WARRANTSNAPSHOTEXDATA,
  __module__ = 'Qot_GetSecuritySnapshot_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetSecuritySnapshot.WarrantSnapshotExData)
  ))
_sym_db.RegisterMessage(WarrantSnapshotExData)

SnapshotBasicData = _reflection.GeneratedProtocolMessageType('SnapshotBasicData', (_message.Message,), dict(
  DESCRIPTOR = _SNAPSHOTBASICDATA,
  __module__ = 'Qot_GetSecuritySnapshot_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetSecuritySnapshot.SnapshotBasicData)
  ))
_sym_db.RegisterMessage(SnapshotBasicData)

Snapshot = _reflection.GeneratedProtocolMessageType('Snapshot', (_message.Message,), dict(
  DESCRIPTOR = _SNAPSHOT,
  __module__ = 'Qot_GetSecuritySnapshot_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetSecuritySnapshot.Snapshot)
  ))
_sym_db.RegisterMessage(Snapshot)

S2C = _reflection.GeneratedProtocolMessageType('S2C', (_message.Message,), dict(
  DESCRIPTOR = _S2C,
  __module__ = 'Qot_GetSecuritySnapshot_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetSecuritySnapshot.S2C)
  ))
_sym_db.RegisterMessage(S2C)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'Qot_GetSecuritySnapshot_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetSecuritySnapshot.Request)
  ))
_sym_db.RegisterMessage(Request)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'Qot_GetSecuritySnapshot_pb2'
  # @@protoc_insertion_point(class_scope:Qot_GetSecuritySnapshot.Response)
  ))
_sym_db.RegisterMessage(Response)


# @@protoc_insertion_point(module_scope)
