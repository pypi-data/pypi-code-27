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

u"""Quantum gates that are commonly used in the literature."""
from __future__ import absolute_import
import math
from typing import Union, Tuple, Optional, List, Callable, cast, Iterable

import numpy as np

from cirq import value
from cirq.ops import gate_features, eigen_gate, raw_types, gate_operation
from itertools import izip


class Rot11Gate(eigen_gate.EigenGate,
                gate_features.PhaseableEffect,
                gate_features.TwoQubitGate,
                gate_features.TextDiagrammable,
                gate_features.InterchangeableQubitsGate,
                gate_features.QasmConvertableGate):
    u"""Phases the |11> state of two adjacent qubits by a fixed amount.

    A ParameterizedCZGate guaranteed to not be using the parameter key field.
    """

    def __init__(self, **_3to2kwargs):
        if 'degs' in _3to2kwargs: degs = _3to2kwargs['degs']; del _3to2kwargs['degs']
        else: degs =  None
        if 'rads' in _3to2kwargs: rads = _3to2kwargs['rads']; del _3to2kwargs['rads']
        else: rads =  None
        if 'half_turns' in _3to2kwargs: half_turns = _3to2kwargs['half_turns']; del _3to2kwargs['half_turns']
        else: half_turns =  None
        u"""Initializes the gate.

        At most one angle argument may be specified. If more are specified,
        the result is considered ambiguous and an error is thrown. If no angle
        argument is given, the default value of one half turn is used.

        Args:
            half_turns: Relative phasing of CZ's eigenstates, in half_turns.
            rads: Relative phasing of CZ's eigenstates, in radians.
            degs: Relative phasing of CZ's eigenstates, in degrees.
        """
        super(Rot11Gate, self).__init__(exponent=value.chosen_angle_to_half_turns(
            half_turns=half_turns,
            rads=rads,
            degs=degs))

    def _eigen_components(self):
        return [
            (0, np.diag([1, 1, 1, 0])),
            (1, np.diag([0, 0, 0, 1])),
        ]

    def _canonical_exponent_period(self):
        return 2

    def _with_exponent(self,
                       exponent):
        return Rot11Gate(half_turns=exponent)

    def phase_by(self, phase_turns, qubit_index):
        return self

    @property
    def half_turns(self):
        return self._exponent

    def text_diagram_info(self, args
                          ):
        return gate_features.TextDiagramInfo(
            wire_symbols=(u'@', u'@'),
            exponent=self._exponent)

    def known_qasm_output(self,
                          qubits,
                          args):
        if self.half_turns != 1:
            return None  # Don't have an equivalent gate in QASM
        args.validate_version(u'2.0')
        return args.format(u'cz {0},{1};\n', qubits[0], qubits[1])

    def __repr__(self):
        if self.half_turns == 1:
            return u'CZ'
        return u'CZ**{!r}'.format(self.half_turns)


class RotXGate(eigen_gate.EigenGate,
               gate_features.TextDiagrammable,
               gate_features.SingleQubitGate,
               gate_features.QasmConvertableGate):
    u"""Fixed rotation around the X axis of the Bloch sphere."""

    def __init__(self, **_3to2kwargs):
        if 'degs' in _3to2kwargs: degs = _3to2kwargs['degs']; del _3to2kwargs['degs']
        else: degs =  None
        if 'rads' in _3to2kwargs: rads = _3to2kwargs['rads']; del _3to2kwargs['rads']
        else: rads =  None
        if 'half_turns' in _3to2kwargs: half_turns = _3to2kwargs['half_turns']; del _3to2kwargs['half_turns']
        else: half_turns =  None
        u"""Initializes the gate.

        At most one angle argument may be specified. If more are specified,
        the result is considered ambiguous and an error is thrown. If no angle
        argument is given, the default value of one half turn is used.

        Args:
            half_turns: The relative phasing of X's eigenstates, in half_turns.
            rads: The relative phasing of X's eigenstates, in radians.
            degs: The relative phasing of X's eigenstates, in degrees.
        """
        super(RotXGate, self).__init__(exponent=value.chosen_angle_to_half_turns(
            half_turns=half_turns,
            rads=rads,
            degs=degs))

    def _eigen_components(self):
        return [
            (0, np.array([[0.5, 0.5], [0.5, 0.5]])),
            (1, np.array([[0.5, -0.5], [-0.5, 0.5]])),
        ]

    def _canonical_exponent_period(self):
        return 2

    def _with_exponent(self,
                       exponent):
        return RotXGate(half_turns=exponent)

    @property
    def half_turns(self):
        return self._exponent

    def text_diagram_info(self, args
                          ):
        return gate_features.TextDiagramInfo(
            wire_symbols=(u'X',),
            exponent=self._exponent)

    def known_qasm_output(self,
                          qubits,
                          args):
        args.validate_version(u'2.0')
        if self.half_turns == 1:
            return args.format(u'x {0};\n', qubits[0])
        else:
            return args.format(u'rx({0:half_turns}) {1};\n',
                               self.half_turns, qubits[0])

    def __repr__(self):
        if self.half_turns == 1:
            return u'X'
        return u'X**{!r}'.format(self.half_turns)


class RotYGate(eigen_gate.EigenGate,
               gate_features.TextDiagrammable,
               gate_features.SingleQubitGate,
               gate_features.QasmConvertableGate):
    u"""Fixed rotation around the Y axis of the Bloch sphere."""

    def __init__(self, **_3to2kwargs):
        if 'degs' in _3to2kwargs: degs = _3to2kwargs['degs']; del _3to2kwargs['degs']
        else: degs =  None
        if 'rads' in _3to2kwargs: rads = _3to2kwargs['rads']; del _3to2kwargs['rads']
        else: rads =  None
        if 'half_turns' in _3to2kwargs: half_turns = _3to2kwargs['half_turns']; del _3to2kwargs['half_turns']
        else: half_turns =  None
        u"""Initializes the gate.

        At most one angle argument may be specified. If more are specified,
        the result is considered ambiguous and an error is thrown. If no angle
        argument is given, the default value of one half turn is used.

        Args:
            half_turns: The relative phasing of Y's eigenstates, in half_turns.
            rads: The relative phasing of Y's eigenstates, in radians.
            degs: The relative phasing of Y's eigenstates, in degrees.
        """
        super(RotYGate, self).__init__(exponent=value.chosen_angle_to_half_turns(
            half_turns=half_turns,
            rads=rads,
            degs=degs))

    def _eigen_components(self):
        return [
            (0, np.array([[0.5, -0.5j], [0.5j, 0.5]])),
            (1, np.array([[0.5, 0.5j], [-0.5j, 0.5]])),
        ]

    def _canonical_exponent_period(self):
        return 2

    def _with_exponent(self,
                       exponent):
        return RotYGate(half_turns=exponent)

    @property
    def half_turns(self):
        return self._exponent

    def text_diagram_info(self, args
                          ):
        return gate_features.TextDiagramInfo(
            wire_symbols=(u'Y',),
            exponent=self._exponent)

    def known_qasm_output(self,
                          qubits,
                          args):
        args.validate_version(u'2.0')
        if self.half_turns == 1:
            return args.format(u'y {0};\n', qubits[0])
        else:
            return args.format(u'ry({0:half_turns}) {1};\n',
                               self.half_turns, qubits[0])

    def __repr__(self):
        if self.half_turns == 1:
            return u'Y'
        return u'Y**{!r}'.format(self.half_turns)


class RotZGate(eigen_gate.EigenGate,
               gate_features.TextDiagrammable,
               gate_features.SingleQubitGate,
               gate_features.PhaseableEffect,
               gate_features.QasmConvertableGate):
    u"""Fixed rotation around the Z axis of the Bloch sphere."""

    def __init__(self, **_3to2kwargs):
        if 'degs' in _3to2kwargs: degs = _3to2kwargs['degs']; del _3to2kwargs['degs']
        else: degs =  None
        if 'rads' in _3to2kwargs: rads = _3to2kwargs['rads']; del _3to2kwargs['rads']
        else: rads =  None
        if 'half_turns' in _3to2kwargs: half_turns = _3to2kwargs['half_turns']; del _3to2kwargs['half_turns']
        else: half_turns =  None
        u"""Initializes the gate.

        At most one angle argument may be specified. If more are specified,
        the result is considered ambiguous and an error is thrown. If no angle
        argument is given, the default value of one half turn is used.

        Args:
            half_turns: The relative phasing of Z's eigenstates, in half_turns.
            rads: The relative phasing of Z's eigenstates, in radians.
            degs: The relative phasing of Z's eigenstates, in degrees.
        """
        super(RotZGate, self).__init__(exponent=value.chosen_angle_to_half_turns(
            half_turns=half_turns,
            rads=rads,
            degs=degs))

    def _eigen_components(self):
        return [
            (0, np.diag([1, 0])),
            (1, np.diag([0, 1])),
        ]

    def _canonical_exponent_period(self):
        return 2

    def _with_exponent(self,
                       exponent):
        return RotZGate(half_turns=exponent)

    @property
    def half_turns(self):
        return self._exponent

    def phase_by(self,
                 phase_turns,
                 qubit_index):
        return self

    def text_diagram_info(self, args
                          ):
        if self.half_turns in [-0.25, 0.25]:
            return gate_features.TextDiagramInfo(
                wire_symbols=(u'T',),
                exponent=cast(float, self._exponent) * 4)

        if self.half_turns in [-0.5, 0.5]:
            return gate_features.TextDiagramInfo(
                wire_symbols=(u'S',),
                exponent=cast(float, self._exponent) * 2)

        return gate_features.TextDiagramInfo(
            wire_symbols=(u'Z',),
            exponent=self._exponent)

    def known_qasm_output(self,
                          qubits,
                          args):
        args.validate_version(u'2.0')
        if self.half_turns == 1:
            return args.format(u'z {0};\n', qubits[0])
        else:
            return args.format(u'rz({0:half_turns}) {1};\n',
                               self.half_turns, qubits[0])

    def __repr__(self):
        if self.half_turns == 0.25:
            return u'T'
        if self.half_turns == -0.25:
            return u'T**-1'
        if self.half_turns == 0.5:
            return u'S'
        if self.half_turns == -0.5:
            return u'S**-1'
        if self.half_turns == 1:
            return u'Z'
        return u'Z**{!r}'.format(self.half_turns)


class MeasurementGate(raw_types.Gate,
                      gate_features.TextDiagrammable,
                      gate_features.QasmConvertableGate):
    u"""Indicates that qubits should be measured plus a key to identify results.

    Attributes:
        key: The string key of the measurement.
        invert_mask: A list of values indicating whether the corresponding
            qubits should be flipped. The list's length must not be longer than
            the number of qubits, but it is permitted to be shorted. Qubits with
            indices past the end of the mask are not flipped.
    """

    def __init__(self,
                 key = u'',
                 invert_mask = ()):
        self.key = key
        self.invert_mask = invert_mask or ()

    @staticmethod
    def is_measurement(op):
        if isinstance(op, MeasurementGate):
            return True
        if (isinstance(op, gate_operation.GateOperation) and
                isinstance(op.gate, MeasurementGate)):
            return True
        return False

    def with_bits_flipped(self, *bit_positions):
        u"""Toggles whether or not the measurement inverts various outputs."""
        old_mask = self.invert_mask or ()
        n = max(len(old_mask) - 1, *bit_positions) + 1
        new_mask = [k < len(old_mask) and old_mask[k] for k in xrange(n)]
        for b in bit_positions:
            new_mask[b] = not new_mask[b]
        return MeasurementGate(key=self.key, invert_mask=tuple(new_mask))

    def validate_args(self, qubits):
        if (self.invert_mask is not None and
                len(self.invert_mask) > len(qubits)):
            raise ValueError(u'len(invert_mask) > len(qubits)')

    def text_diagram_info(self, args
                          ):
        n = (max(1, len(self.invert_mask))
             if args.known_qubit_count is None
             else args.known_qubit_count)
        symbols = [u'M'] * n

        # Show which output bits are negated.
        if self.invert_mask:
            for i, b in enumerate(self.invert_mask):
                if b:
                    symbols[i] = u'!M'

        # Mention the measurement key.
        if (not args.known_qubits or
                self.key != _default_measurement_key(args.known_qubits)):
            symbols[0] += u"('{}')".format(self.key)

        return gate_features.TextDiagramInfo(tuple(symbols))

    def known_qasm_output(self,
                          qubits,
                          args):
        args.validate_version(u'2.0')
        invert_mask = self.invert_mask
        if len(invert_mask) < len(qubits):
            invert_mask = (invert_mask
                           + (False,) * (len(qubits) - len(invert_mask)))
        lines = []
        for i, (qubit, inv) in enumerate(izip(qubits, invert_mask)):
            if inv:
                lines.append(args.format(
                        u'x {0};  // Invert the following measurement\n', qubit))
            lines.append(args.format(u'measure {0} -> {1:meas}[{2}];\n',
                                     qubit, self.key, i))
        return u''.join(lines)

    def __repr__(self):
        return u'MeasurementGate({}, {})'.format(repr(self.key),
                                                repr(self.invert_mask))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.key == other.key and self.invert_mask == other.invert_mask

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((MeasurementGate, self.key, self.invert_mask))


def _default_measurement_key(qubits):
    return u','.join(unicode(q) for q in qubits)


def measure(*qubits, **_3to2kwargs
            ):
    if 'invert_mask' in _3to2kwargs: invert_mask = _3to2kwargs['invert_mask']; del _3to2kwargs['invert_mask']
    else: invert_mask =  ()
    if 'key' in _3to2kwargs: key = _3to2kwargs['key']; del _3to2kwargs['key']
    else: key =  None
    u"""Returns a single MeasurementGate applied to all the given qubits.

    The qubits are measured in the computational basis.

    Args:
        *qubits: The qubits that the measurement gate should measure.
        key: The string key of the measurement. If this is None, it defaults
            to a comma-separated list of the target qubits' str values.
        invert_mask: A list of Truthy or Falsey values indicating whether
            the corresponding qubits should be flipped. None indicates no
            inverting should be done.

    Returns:
        An operation targeting the given qubits with a measurement.
    """
    if key is None:
        key = _default_measurement_key(qubits)
    return MeasurementGate(key, invert_mask).on(*qubits)


def measure_each(*qubits, **_3to2kwargs
                 ):
    if 'key_func' in _3to2kwargs: key_func = _3to2kwargs['key_func']; del _3to2kwargs['key_func']
    else: key_func =  unicode
    u"""Returns a list of operations individually measuring the given qubits.

    The qubits are measured in the computational basis.

    Args:
        *qubits: The qubits to measure.
        key_func: Determines the key of the measurements of each qubit. Takes
            the qubit and returns the key for that qubit. Defaults to str.

    Returns:
        A list of operations individually measuring the given qubits.
    """
    return [MeasurementGate(key_func(q)).on(q) for q in qubits]


X = RotXGate()  # Pauli X gate.
Y = RotYGate()  # Pauli Y gate.
Z = RotZGate()  # Pauli Z gate.
CZ = Rot11Gate()  # Negates the amplitude of the |11> state.

S = Z**0.5
T = Z**0.25


class HGate(gate_features.CompositeGate,
            gate_features.TextDiagrammable,
            gate_features.ReversibleEffect,
            gate_features.KnownMatrix,
            gate_features.SingleQubitGate,
            gate_features.QasmConvertableGate):
    u"""180 degree rotation around the X+Z axis of the Bloch sphere."""

    def text_diagram_info(self, args
                          ):
        return gate_features.TextDiagramInfo((u'H',))

    def default_decompose(self, qubits):
        q = qubits[0]
        yield Y(q)**0.5
        yield X(q)

    def inverse(self):
        return self

    def matrix(self):
        u"""See base class."""
        s = math.sqrt(0.5)
        return np.array([[s, s], [s, -s]])

    def known_qasm_output(self,
                          qubits,
                          args):
        args.validate_version(u'2.0')
        return args.format(u'h {0};\n', qubits[0])

    def __repr__(self):
        return u'H'


H = HGate()  # Hadamard gate.


class CNotGate(eigen_gate.EigenGate,
               gate_features.TextDiagrammable,
               gate_features.CompositeGate,
               gate_features.TwoQubitGate,
               gate_features.QasmConvertableGate):
    u"""A controlled-NOT. Toggle the second qubit when the first qubit is on."""

    def __init__(self, **_3to2kwargs):
        if 'degs' in _3to2kwargs: degs = _3to2kwargs['degs']; del _3to2kwargs['degs']
        else: degs =  None
        if 'rads' in _3to2kwargs: rads = _3to2kwargs['rads']; del _3to2kwargs['rads']
        else: rads =  None
        if 'half_turns' in _3to2kwargs: half_turns = _3to2kwargs['half_turns']; del _3to2kwargs['half_turns']
        else: half_turns =  None
        u"""Initializes the gate.

        At most one angle argument may be specified. If more are specified,
        the result is considered ambiguous and an error is thrown. If no angle
        argument is given, the default value of one half turn is used.

        Args:
            half_turns: Relative phasing of CNOT's eigenstates, in half_turns.
            rads: Relative phasing of CNOT's eigenstates, in radians.
            degs: Relative phasing of CNOT's eigenstates, in degrees.
        """
        super(CNotGate, self).__init__(exponent=value.chosen_angle_to_half_turns(
            half_turns=half_turns,
            rads=rads,
            degs=degs))

    def default_decompose(self, qubits):
        c, t = qubits
        yield Y(t)**-0.5
        yield Rot11Gate(half_turns=self.half_turns).on(c, t)
        yield Y(t)**0.5

    def _eigen_components(self):
        return [
            (0, np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0.5, 0.5],
                          [0, 0, 0.5, 0.5]])),
            (1, np.array([[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0.5, -0.5],
                          [0, 0, -0.5, 0.5]])),
        ]

    def _canonical_exponent_period(self):
        return 2

    def _with_exponent(self,
                       exponent):
        return CNotGate(half_turns=exponent)

    @property
    def half_turns(self):
        return self._exponent

    def text_diagram_info(self, args
                          ):
        return gate_features.TextDiagramInfo(
            wire_symbols=(u'@', u'X'),
            exponent=self._exponent)

    def known_qasm_output(self,
                          qubits,
                          args):
        if self.half_turns != 1:
            return None  # Don't have an equivalent gate in QASM
        args.validate_version(u'2.0')
        return args.format(u'cx {0},{1};\n', qubits[0], qubits[1])

    def __repr__(self):
        if self.half_turns == 1:
            return u'CNOT'
        return u'CNOT**{!r}'.format(self.half_turns)


CNOT = CNotGate()  # Controlled Not Gate.


class SwapGate(eigen_gate.EigenGate,
               gate_features.TextDiagrammable,
               gate_features.TwoQubitGate,
               gate_features.CompositeGate,
               gate_features.InterchangeableQubitsGate,
               gate_features.QasmConvertableGate):
    u"""Swaps two qubits."""

    def __init__(self, **_3to2kwargs):
        if 'half_turns' in _3to2kwargs: half_turns = _3to2kwargs['half_turns']; del _3to2kwargs['half_turns']
        else: half_turns =  1.0
        super(SwapGate, self).__init__(exponent=half_turns)

    def default_decompose(self, qubits):
        u"""See base class."""
        a, b = qubits
        yield CNOT(a, b)
        yield CNOT(b, a) ** self.half_turns
        yield CNOT(a, b)

    def _eigen_components(self):
        return [
            (0, np.array([[1, 0,   0,   0],
                          [0, 0.5, 0.5, 0],
                          [0, 0.5, 0.5, 0],
                          [0, 0,   0,   1]])),
            (1, np.array([[0,  0,    0,   0],
                          [0,  0.5, -0.5, 0],
                          [0, -0.5,  0.5, 0],
                          [0,  0,    0,   0]])),
        ]

    def _canonical_exponent_period(self):
        return 2

    def _with_exponent(self,
                       exponent):
        return SwapGate(half_turns=exponent)

    @property
    def half_turns(self):
        return self._exponent

    def text_diagram_info(self, args
                          ):
        if not args.use_unicode_characters:
            return gate_features.TextDiagramInfo(
                wire_symbols=(u'swap', u'swap'),
                exponent=self._exponent)
        return gate_features.TextDiagramInfo(
            wire_symbols=(u'×', u'×'),
            exponent=self._exponent)

    def known_qasm_output(self,
                          qubits,
                          args):
        if self.half_turns != 1:
            return None  # Don't have an equivalent gate in QASM
        args.validate_version(u'2.0')
        return args.format(u'swap {0},{1};\n', qubits[0], qubits[1])

    def __repr__(self):
        if self.half_turns == 1:
            return u'SWAP'
        return u'SWAP**{!r}'.format(self.half_turns)


SWAP = SwapGate()  # Exchanges two qubits' states.


class ISwapGate(eigen_gate.EigenGate,
                gate_features.CompositeGate,
                gate_features.InterchangeableQubitsGate,
                gate_features.TextDiagrammable,
                gate_features.TwoQubitGate):
    u"""Rotates the |01⟩-vs-|10⟩ subspace of two qubits around its Bloch X-axis.

    When exponent=1, swaps the two qubits and phases |01⟩ and |10⟩ by i. More
    generally, this gate's matrix is defined as follows:

        ISWAP**t ≡ exp(+i π t (X⊗X + Y⊗Y) / 4)
                 ≡ [1 0            0            0]
                   [0 cos(π·t/2)   i·sin(π·t/2) 0]
                   [0 i·sin(π·t/2) cos(π·t/2)   0]
                   [0 0            0            1]
    """

    @property
    def exponent(self):
        return self._exponent

    def _eigen_components(self):
        return [
            (0, np.diag([1, 0, 0, 1])),
            (+0.5, np.array([[0, 0, 0, 0],
                             [0, 0.5, 0.5, 0],
                             [0, 0.5, 0.5, 0],
                             [0, 0, 0, 0]])),
            (-0.5, np.array([[0, 0, 0, 0],
                             [0, 0.5, -0.5, 0],
                             [0, -0.5, 0.5, 0],
                             [0, 0, 0, 0]])),
        ]

    def _canonical_exponent_period(self):
        return 4

    def _with_exponent(self, exponent
                       ):
        return ISwapGate(exponent=exponent)

    def default_decompose(self, qubits):
        a, b = qubits

        yield CNOT(a, b)
        yield H(a)
        yield CNOT(b, a)
        yield S(a)**self.exponent
        yield CNOT(b, a)
        yield S(a)**-self.exponent
        yield H(a)
        yield CNOT(a, b)

    def text_diagram_info(self, args
                          ):
        return gate_features.TextDiagramInfo(
            wire_symbols=(u'iSwap', u'iSwap'),
            exponent=self._exponent)

    def __repr__(self):
        if self.exponent == 1:
            return u'ISWAP'
        return u'ISWAP**{!r}'.format(self.exponent)


ISWAP = ISwapGate()  # Swaps two qubits while phasing the swapped subspace by i.
