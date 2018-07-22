# Copyright (C) 2018  KINA Open
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./moonshade.proto

import moonshade_pb2
import moonshade_pb2_grpc
import grpc


class Client:
    def __init__(self, address, username, password):
        self.channel = grpc.insecure_channel(address)
        self.username = username
        self.password = password
        self.documentStub = moonshade_pb2_grpc.documentStub(self.channel)

    def find_one(self, storage, db, coll, flt):
        reply = self.documentStub.FindOne(moonshade_pb2.FindOneRequest(
            token=moonshade_pb2.Token(username=self.username, password=self.password, storage=storage, database=db,
                                      collection=coll), filter=flt))
        return reply.result, reply.code

    def delete_one(self, storage, db, coll, flt):
        reply = self.documentStub.DeleteOne(moonshade_pb2.DeleteOneRequest(
            token=moonshade_pb2.Token(username=self.username, password=self.password, storage=storage, database=db,
                                      collection=coll), filter=flt))
        return reply.result, reply.code

    def insert_one(self, storage, db, coll, doc):
        reply = self.documentStub.InsertOne(moonshade_pb2.InsertOneRequest(
            token=moonshade_pb2.Token(username=self.username, password=self.password, storage=storage, database=db,
                                      collection=coll), document=doc))
        return reply.result, reply.code

    def replace_one(self, storage, db, coll, flt, doc):
        reply = self.documentStub.ReplaceOne(moonshade_pb2.ReplaceOneRequest(
            token=moonshade_pb2.Token(username=self.username, password=self.password, storage=storage, database=db,
                                      collection=coll), filter=flt, replace=doc))
        return reply.result, reply.code

    def update_one(self, storage, db, coll, flt, doc):
        reply = self.documentStub.UpdateOne(moonshade_pb2.UpdateOneRequest(
            token=moonshade_pb2.Token(username=self.username, password=self.password, storage=storage, database=db,
                                      collection=coll), filter=flt, update=doc))
        return reply.result, reply.code
