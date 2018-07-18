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

from __future__ import absolute_import
from cirq import circuits, extension, ops
from cirq.contrib.qcircuit.qcircuit_diagrammable import (
    QCircuitDiagrammable,
    fallback_qcircuit_extensions,
)


class _QCircuitQubit(ops.QubitId):
    def __init__(self, sub):
        self.sub = sub

    def __repr__(self):
        return u'_QCircuitQubit({!r})'.format(self.sub)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        # TODO: If qubit name ends with digits, turn them into subscripts.
        return u'\\lstick{\\text{' + unicode(self.sub) + u'}}&'

    def __eq__(self, other):
        if not isinstance(other, _QCircuitQubit):
            return NotImplemented
        return self.sub == other.sub

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((_QCircuitQubit, self.sub))


class _QCircuitOperation(ops.Operation, ops.TextDiagrammable):
    def __init__(self,
                 sub_operation,
                 diagrammable):
        self.sub_operation = sub_operation
        self.diagrammable = diagrammable

    def text_diagram_info(self, args
                          ):
        return ops.TextDiagramInfo(
            self.diagrammable.qcircuit_diagram_info(args))

    @property
    def qubits(self):
        return self.sub_operation.qubits

    def with_qubits(self, *new_qubits):
        return _QCircuitOperation(
            self.sub_operation.with_qubits(*new_qubits),
            self.diagrammable)


def _render(diagram):
    w = diagram.width()
    h = diagram.height()

    qwx = set([(x, y + 1)
           for x, y1, y2, _ in diagram.vertical_lines
           for y in xrange(y1, y2)])

    qw = set([(x, y)
          for y, x1, x2, _ in diagram.horizontal_lines
          for x in xrange(x1, x2)])

    rows = []
    for y in xrange(h):
        row = []
        for x in xrange(w):
            cell = []
            key = (x, y)
            v = diagram.entries.get(key)
            if v is not None:
                cell.append(u' ' + v + u' ')
            if key in qw:
                cell.append(u'\\qw ')
            if key in qwx:
                cell.append(u'\\qwx ')
            row.append(u''.join(cell))
        rows.append(u'&'.join(row) + u'\qw')

    grid = u'\\\\\n'.join(rows)

    output = u'\Qcircuit @R=1em @C=0.75em { \\\\ \n' + grid + u' \\\\ \n \\\\ }'

    return output


def _wrap_operation(op,
                    ext):
    new_qubits = [_QCircuitQubit(e) for e in op.qubits]
    diagrammable = ext.try_cast(QCircuitDiagrammable, op)
    if diagrammable is None:
        diagrammable = fallback_qcircuit_extensions.cast(
            QCircuitDiagrammable, op)
    return _QCircuitOperation(op, diagrammable).with_qubits(*new_qubits)


def _wrap_moment(moment,
                 ext):
    return circuits.Moment(_wrap_operation(op, ext)
                           for op in moment.operations)


def _wrap_circuit(circuit,
                  ext):
    return circuits.Circuit(_wrap_moment(moment, ext)
                            for moment in circuit)


def circuit_to_latex_using_qcircuit(
        circuit,
        ext = None,
        qubit_order = ops.QubitOrder.DEFAULT):
    u"""Returns a QCircuit-based latex diagram of the given circuit.

    Args:
        circuit: The circuit to represent in latex.
        ext: Extensions used when attempting to cast gates into
            QCircuitDiagrammable instances (before falling back to the
            default wrapping methods).
        qubit_order: Determines the order of qubit wires in the diagram.

    Returns:
        Latex code for the diagram.
    """
    if ext is None:
        ext = extension.Extensions()
    qcircuit = _wrap_circuit(circuit, ext)

    # Note: can't be a lambda because we need the type hint.
    def get_sub(q):
        return q.sub

    diagram = qcircuit.to_text_diagram_drawer(
        ext,
        qubit_name_suffix=u'',
        qubit_order=ops.QubitOrder.as_qubit_order(qubit_order).map(
            internalize=get_sub, externalize=_QCircuitQubit))
    return _render(diagram)
