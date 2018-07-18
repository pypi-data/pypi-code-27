# coding=utf-8
# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

u"""An optimization pass that combines adjacent single-qubit rotations."""

from __future__ import with_statement
from __future__ import division
from __future__ import absolute_import
from typing import Set  # pylint: disable=unused-import
from typing import (
    Callable, Dict, Optional, Sequence, Tuple, Union, cast
)

import re
import numpy as np

from cirq import ops, linalg, extension
from io import open
from itertools import imap


class QasmUGate(ops.SingleQubitGate, ops.QasmConvertableGate):
    def __init__(self, lmda, theta, phi):
        u"""A QASM gate representing any single qubit unitary with a series of
        three rotations, Z, Y, and Z.

        The angles are normalized to the range [0, 2) half_turns.

        Args:
            lmda: Half turns to rotate about Z (applied first).
            theta: Half turns to rotate about Y.
            phi: Half turns to rotate about Z (applied last).
        """
        self.lmda = lmda % 2
        self.theta = theta % 2
        self.phi = phi % 2

    @staticmethod
    def from_matrix(mat):
        pre_phase, rotation, post_phase = (
            linalg.deconstruct_single_qubit_matrix_into_angles(mat))
        return QasmUGate(pre_phase/np.pi, rotation/np.pi, post_phase/np.pi)

    def known_qasm_output(self,
                          qubits,
                          args):
        args.validate_version(u'2.0')
        return args.format(
                u'u3({0:half_turns},{1:half_turns},{2:half_turns}) {3};\n',
                self.theta, self.phi, self.lmda, qubits[0])

    def __repr__(self):
        return u'QasmUGate({}, {}, {})'.format(self.lmda, self.theta, self.phi)


class QasmTwoQubitGate(ops.TwoQubitGate, ops.CompositeGate):
    def __init__(self,
                 before0,
                 before1,
                 x, y, z,
                 after0,
                 after1):
        u"""A two qubit gate represented in QASM by the KAK decomposition.

        All angles are in half turns.  Assumes a canonicalized KAK
        decomposition.

        Args:
            before0: Gate applied to qubit 0 before the interaction.
            before1: Gate applied to qubit 1 before the interaction.
            x: XX interaction.
            y: YY interaction.
            z: ZZ interaction.
            after0: Gate applied to qubit 0 after the interaction.
            after1: Gate applied to qubit 1 after the interaction.
        """
        self.before0 = before0
        self.before1 = before1
        self.x, self.y, self.z = x, y, z
        self.after0 = after0
        self.after1 = after1

    @staticmethod
    def from_matrix(mat, tolerance=1e-8):
        _, (a1, a0), (x, y, z), (b1, b0) = linalg.kak_decomposition(
            mat,
            linalg.Tolerance(atol=tolerance))
        before0 = QasmUGate.from_matrix(b0)
        before1 = QasmUGate.from_matrix(b1)
        after0 = QasmUGate.from_matrix(a0)
        after1 = QasmUGate.from_matrix(a1)
        return QasmTwoQubitGate(before0, before1,
                                x, y, z,
                                after0, after1)

    def default_decompose(self, qubits):
        q0, q1 = qubits
        a = self.x * -2 / np.pi + 0.5
        b = self.y * -2 / np.pi + 0.5
        c = self.z * -2 / np.pi + 0.5

        yield self.before0(q0)
        yield self.before1(q1)

        yield ops.X(q0)**0.5
        yield ops.CNOT(q0, q1)
        yield ops.X(q0)**a
        yield ops.Y(q1)**b
        yield ops.CNOT(q1, q0)
        yield ops.X(q1)**-0.5
        yield ops.Z(q1)**c
        yield ops.CNOT(q0, q1)

        yield self.after0(q0)
        yield self.after1(q1)

    def __repr__(self):
        return u'QasmTwoQubitGate({}, {}, {}, {}, {}, {}, {})'.format(
                self.before0, self.before1, self.x, self.y, self.z,
                self.after0, self.after1)


class QasmOutput(object):
    valid_id_re = re.compile(u'[a-z][a-zA-Z0-9_]*\Z')

    def __init__(self,
                 operations,
                 qubits,
                 header = u'',
                 precision = 10,
                 version = u'2.0',
                 ext = None):
        self.operations = tuple(ops.flatten_op_tree(operations))
        self.qubits = qubits
        self.header = header
        if ext is None:
            ext = extension.Extensions()
        self.ext = ext
        self.measurements = tuple(cast(ops.GateOperation, op)
                                  for op in self.operations
                                  if ops.MeasurementGate.is_measurement(op))

        meas_key_id_map, meas_comments = self._generate_measurement_ids()
        self.meas_comments = meas_comments
        qubit_id_map = self._generate_qubit_ids()
        self.args = ops.QasmOutputArgs(precision=precision,
                                       version=version,
                                       qubit_id_map=qubit_id_map,
                                       meas_key_id_map=meas_key_id_map)

    def _generate_measurement_ids(self
            ):
        # Pick an id for the creg that will store each measurement
        meas_key_id_map = {}  # type: Dict[str, str]
        meas_comments = {}  # type: Dict[str, Optional[str]]
        meas_i = 0
        for meas in self.measurements:
            key = cast(ops.MeasurementGate, meas.gate).key
            if key in meas_key_id_map:
                continue
            meas_id = u'm_{}'.format(key)
            if self.is_valid_qasm_id(meas_id):
                meas_comments[key] = None
            else:
                meas_id = u'm{}'.format(meas_i)
                meas_i += 1
                meas_comments[key] = u' '.join(key.split(u'\n'))
            meas_key_id_map[key] = meas_id
        return meas_key_id_map, meas_comments

    def _generate_qubit_ids(self):
        return dict((qubit, u'q[{}]'.format(i)) for i, qubit in enumerate(self.qubits))

    def is_valid_qasm_id(self, id_str):
        u"""Test if id_str is a valid id in QASM grammar."""
        return self.valid_id_re.match(id_str) != None

    def save(self, path):
        u"""Write QASM output to a file specified by path."""
        with open(path, u'w') as f:
            def write(s):
                f.write(s)
            self._write_qasm(write)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        u"""Return QASM output as a string."""
        output = []
        self._write_qasm(lambda s:output.append(s))
        return u''.join(output)

    def _write_qasm(self, output_func):
        self.args.validate_version(u'2.0')

        # Generate nice line spacing
        line_gap = [0]
        def output_line_gap(n):
            line_gap[0] = max(line_gap[0], n)
        def output(text):
            if line_gap[0] > 0:
                output_func(u'\n' * line_gap[0])
                line_gap[0] = 0
            output_func(text)

        # Comment header
        if self.header:
            for line in self.header.split(u'\n'):
                output((u'// ' + line).rstrip() + u'\n')
            output(u'\n')

        # Version
        output(u'OPENQASM 2.0;\n')
        output(u'include "qelib1.inc";\n')
        output_line_gap(2)

        # Function definitions
        # None yet

        # Register definitions
        # Qubit registers
        output(u'// Qubits: [{}]\n'.format(u', '.join(imap(unicode, self.qubits))))
        output(u'qreg q[{}];\n'.format(len(self.qubits)))
        # Classical registers
        # Pick an id for the creg that will store each measurement
        already_output_keys = set()  # type: Set[str]
        for meas in self.measurements:
            key = cast(ops.MeasurementGate, meas.gate).key
            if key in already_output_keys:
                continue
            already_output_keys.add(key)
            meas_id = self.args.meas_key_id_map[key]
            comment = self.meas_comments[key]
            if comment is None:
                output(u'creg {}[{}];\n'.format(meas_id, len(meas.qubits)))
            else:
                output(u'creg {}[{}];  // Measurement: {}\n'.format(
                            meas_id, len(meas.qubits), comment))
        output_line_gap(2)

        # Operations
        self._write_operations(self.operations, output, output_line_gap)

    def _write_operations(self,
                          op_tree,
                          output,
                          output_line_gap,
                          top=True):
        for op in ops.flatten_op_tree(op_tree):
            qasm_op = self.ext.try_cast(ops.QasmConvertableOperation, op)
            if qasm_op is not None:
                out = qasm_op.known_qasm_output(self.args)
                if out is not None:
                    output(out)
                    continue

            if isinstance(op, ops.GateOperation):
                comment = u'Gate: {!s}'.format(op.gate)
            else:
                comment = u'Operation: {!s}'.format(op)
            comp_op = self.ext.try_cast(ops.CompositeOperation, op)
            if comp_op is not None:
                if top:
                    output_line_gap(1)
                    output(u'// {}\n'.format(comment))
                self._write_operations(comp_op.default_decompose(),
                                       output,
                                       output_line_gap,
                                       top=False)
                if top:
                    output_line_gap(1)
                continue

            matrix_op = self.ext.try_cast(ops.KnownMatrix, op)
            if matrix_op is not None and len(op.qubits) == 1:
                u_op = QasmUGate.from_matrix(matrix_op.matrix())(*op.qubits)
                if top:
                    output_line_gap(1)
                    output(u'// {}\n'.format(comment))
                output(u_op.known_qasm_output(self.args))
                if top:
                    output_line_gap(1)
                continue

            if matrix_op is not None and len(op.qubits) == 2:
                u_op = QasmTwoQubitGate.from_matrix(matrix_op.matrix()
                                                    )(*op.qubits)
                if top:
                    output_line_gap(1)
                    output(u'// {}\n'.format(comment))
                self._write_operations((u_op,),
                                       output,
                                       output_line_gap,
                                       top=False)
                if top:
                    output_line_gap(1)
                continue

            raise ValueError(u'Cannot output operation as QASM: {!r}'.format(op))
