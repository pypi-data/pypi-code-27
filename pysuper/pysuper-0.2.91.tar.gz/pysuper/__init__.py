#!/usr/bin/python
# This file is part of Super. A 3D pattern-matching program.
#
# Copyright 2017 James Collier <james.collier412@gmail.com>
#
# Super is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Super is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Super.  If not, see <http://www.gnu.org/licenses/>.

"""Python interface to the super structural fragment search library
"""

from . import _pysuper

name = "pysuper"

class Residue():
    def __init__(self, seqnum, icode, name):
        self._seqnum = seqnum
        self._icode = icode.decode('utf-8')
        self._name = name.decode('utf-8')

    def name(self):
        return self._name

    def position(self):
        return self._icode

    def __repr__(self):
        return f"{self._seqnum}{self._icode}"

class Result():
    def __init__(self, super_object, result):
        self._rmsd = result.rmsd
        self._pdbid = _pysuper.ffi.string(result.ID).decode('utf-8')
        self._chain = result.chain.decode('utf-8')
        query = super_object.query
        meta_begin = _pysuper.lib.db_meta_by_index(super_object.db, \
                                                   result.meta_offset)
        meta_end = \
            _pysuper.lib.db_meta_by_index(super_object.db, \
                                          result.meta_offset \
                                          + result.size - 1)
        self.begin_match = Residue(meta_begin.residueID, \
                                   meta_begin.icode, \
                                   meta_begin.slc)
        self.end_match = Residue(meta_end.residueID, \
                                 meta_end.icode, \
                                 meta_end.slc)
        seq = [_pysuper.lib.db_meta_by_index(super_object.db, \
                                             result.meta_offset + i).slc \
         for i in range(result.size)]
        self.match_seq = b''.join(seq).decode('utf-8')
        self.query_seq = _pysuper.ffi.string(query.sequence).decode('utf-8')

    def __repr__(self):
        return f"{self._pdbid}({self._chain}: {self.begin_match}-{self.end_match}): {self._rmsd} : {self.match_seq}:{self.query_seq}"

    def rmsd(self):
        return self._rmsd

    def pdbid(self):
        return self._pdbid

    def chain(self):
        return self._chain

class Super():
    def __init__(self, query, threshold=2.0):
        self.arguments = _pysuper.ffi.new("struct arguments *")
        self.arguments.verbose = 1
        self.arguments.threads = 1
        self.arguments.coil = 0
        self.arguments.n_query = 1
        self.query = _pysuper.ffi.new("char []", query)
        self.query_list = _pysuper.ffi.new("char **", self.query)
        self.arguments.query = self.query_list
        self.search_database = _pysuper.ffi.new("char []", b"pdb.db")
        self.arguments.search_database = self.search_database
        self.output = _pysuper.ffi.cast("FILE *", open("output.txt", "w"))
        self.arguments.output = self.output
        self.arguments.threshold = threshold

        self.super = _pysuper.ffi.new("struct super_runner *")

    def setup(self):
        return _pysuper.lib.super_runner_setup(self.super, self.arguments)

    def search(self):
        err = _pysuper.lib.super_runner_run(self.super)
        results = []
        res = self.super.results
        while res != _pysuper.ffi.NULL:
            results.append(Result(self.super, res))
            res = res.next
        return err, results
