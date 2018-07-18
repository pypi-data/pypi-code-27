# coding=utf-8
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import absolute_import
import numpy

import openfermion

from openfermioncirq.variational.ansatzes import SwapNetworkTrotterAnsatz


# Construct a Hubbard model Hamiltonian
hubbard_model = openfermion.fermi_hubbard(2, 2, 1., 4.)
hubbard_hamiltonian = openfermion.get_diagonal_coulomb_hamiltonian(
        hubbard_model)

# Construct an empty Hamiltonian
zero_hamiltonian = openfermion.DiagonalCoulombHamiltonian(
        one_body=numpy.zeros((5, 5)),
        two_body=numpy.zeros((5, 5)))


def test_swap_network_trotter_ansatz_parameters():

    ansatz = SwapNetworkTrotterAnsatz(hubbard_hamiltonian)
    assert (set(ansatz.param_names()) ==
            set(ansatz.params.keys()) ==
            set(symbol.name for symbol in ansatz.params.values()) ==
            set([u'T0_2', u'T4_6', u'T1_3', u'T5_7',
             u'T0_4', u'T2_6', u'T1_5', u'T3_7',
             u'V0_1', u'V2_3', u'V4_5', u'V6_7']))

    ansatz = SwapNetworkTrotterAnsatz(hubbard_hamiltonian, iterations=2)
    assert (set(ansatz.param_names()) ==
            set(ansatz.params.keys()) ==
            set(symbol.name for symbol in ansatz.params.values()) ==
            set([u'T0_2-0', u'T4_6-0', u'T1_3-0', u'T5_7-0',
             u'T0_4-0', u'T2_6-0', u'T1_5-0', u'T3_7-0',
             u'V0_1-0', u'V2_3-0', u'V4_5-0', u'V6_7-0',
             u'T0_2-1', u'T4_6-1', u'T1_3-1', u'T5_7-1',
             u'T0_4-1', u'T2_6-1', u'T1_5-1', u'T3_7-1',
             u'V0_1-1', u'V2_3-1', u'V4_5-1', u'V6_7-1']))


def test_swap_network_trotter_ansatz_param_bounds():

    ansatz = SwapNetworkTrotterAnsatz(hubbard_hamiltonian)
    assert ansatz.param_names() == [
            u'V0_1', u'T0_2', u'T0_4', u'T1_3',
            u'T1_5', u'V2_3', u'T2_6', u'T3_7',
            u'V4_5', u'T4_6', u'T5_7', u'V6_7']
    assert ansatz.param_bounds() == [
            (-1.0, 1.0), (-2.0, 2.0), (-2.0, 2.0), (-2.0, 2.0),
            (-2.0, 2.0), (-1.0, 1.0), (-2.0, 2.0), (-2.0, 2.0),
            (-1.0, 1.0), (-2.0, 2.0), (-2.0, 2.0), (-1.0, 1.0)]


def test_swap_network_trotter_ansatz_circuit():

    complete_ansatz = SwapNetworkTrotterAnsatz(
            zero_hamiltonian,
            include_all_xxyy=True,
            include_all_yxxy=True,
            include_all_cz=True,
            include_all_z=True)
    circuit = complete_ansatz.circuit
    assert circuit.to_text_diagram(transpose=True).strip() == u"""
0    1         2         3         4
│    │         │         │         │
XXYY─XXYY^T0_1 XXYY──────XXYY^T2_3 │
│    │         │         │         │
YXXY─#2^W0_1   YXXY──────#2^W2_3   │
│    │         │         │         │
@────@^V0_1    @─────────@^V2_3    │
│    │         │         │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ        │
│    │         │         │         │
│    XXYY──────XXYY^T0_3 XXYY──────XXYY^T2_4
│    │         │         │         │
│    YXXY──────#2^W0_3   YXXY──────#2^W2_4
│    │         │         │         │
│    @─────────@^V0_3    @─────────@^V2_4
│    │         │         │         │
│    ×ᶠ────────×ᶠ        ×ᶠ────────×ᶠ
│    │         │         │         │
XXYY─XXYY^T1_3 XXYY──────XXYY^T0_4 │
│    │         │         │         │
YXXY─#2^W1_3   YXXY──────#2^W0_4   │
│    │         │         │         │
@────@^V1_3    @─────────@^V0_4    │
│    │         │         │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ        │
│    │         │         │         │
│    XXYY──────XXYY^T1_4 XXYY──────XXYY^T0_2
│    │         │         │         │
│    YXXY──────#2^W1_4   YXXY──────#2^W0_2
│    │         │         │         │
│    @─────────@^V1_4    @─────────@^V0_2
│    │         │         │         │
│    ×ᶠ────────×ᶠ        ×ᶠ────────×ᶠ
│    │         │         │         │
XXYY─XXYY^T3_4 XXYY──────XXYY^T1_2 Z^U0
│    │         │         │         │
YXXY─#2^W3_4   YXXY──────#2^W1_2   │
│    │         │         │         │
@────@^V3_4    @─────────@^V1_2    │
│    │         │         │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ        │
│    │         │         │         │
Z^U4 Z^U3      Z^U2      Z^U1      │
│    │         │         │         │
@────@^V3_4    @─────────@^V1_2    │
│    │         │         │         │
#2───YXXY^W3_4 #2────────YXXY^W1_2 │
│    │         │         │         │
XXYY─XXYY^T3_4 XXYY──────XXYY^T1_2 │
│    │         │         │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ        │
│    │         │         │         │
│    @─────────@^V1_4    @─────────@^V0_2
│    │         │         │         │
│    #2────────YXXY^W1_4 #2────────YXXY^W0_2
│    │         │         │         │
│    XXYY──────XXYY^T1_4 XXYY──────XXYY^T0_2
│    │         │         │         │
│    ×ᶠ────────×ᶠ        ×ᶠ────────×ᶠ
│    │         │         │         │
@────@^V1_3    @─────────@^V0_4    │
│    │         │         │         │
#2───YXXY^W1_3 #2────────YXXY^W0_4 │
│    │         │         │         │
XXYY─XXYY^T1_3 XXYY──────XXYY^T0_4 │
│    │         │         │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ        │
│    │         │         │         │
│    @─────────@^V0_3    @─────────@^V2_4
│    │         │         │         │
│    #2────────YXXY^W0_3 #2────────YXXY^W2_4
│    │         │         │         │
│    XXYY──────XXYY^T0_3 XXYY──────XXYY^T2_4
│    │         │         │         │
│    ×ᶠ────────×ᶠ        ×ᶠ────────×ᶠ
│    │         │         │         │
@────@^V0_1    @─────────@^V2_3    │
│    │         │         │         │
#2───YXXY^W0_1 #2────────YXXY^W2_3 │
│    │         │         │         │
XXYY─XXYY^T0_1 XXYY──────XXYY^T2_3 │
│    │         │         │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ        │
│    │         │         │         │
""".strip()

    xxyy_ansatz = SwapNetworkTrotterAnsatz(zero_hamiltonian,
                                           include_all_xxyy=True)
    circuit = xxyy_ansatz.circuit
    assert circuit.to_text_diagram(transpose=True).strip() == u"""
0    1         2         3         4
│    │         │         │         │
XXYY─XXYY^T0_1 XXYY──────XXYY^T2_3 │
│    │         │         │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ        │
│    │         │         │         │
│    XXYY──────XXYY^T0_3 XXYY──────XXYY^T2_4
│    │         │         │         │
│    ×ᶠ────────×ᶠ        ×ᶠ────────×ᶠ
│    │         │         │         │
XXYY─XXYY^T1_3 XXYY──────XXYY^T0_4 │
│    │         │         │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ        │
│    │         │         │         │
│    XXYY──────XXYY^T1_4 XXYY──────XXYY^T0_2
│    │         │         │         │
│    ×ᶠ────────×ᶠ        ×ᶠ────────×ᶠ
│    │         │         │         │
XXYY─XXYY^T3_4 XXYY──────XXYY^T1_2 │
│    │         │         │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ        │
│    │         │         │         │
XXYY─XXYY^T3_4 XXYY──────XXYY^T1_2 │
│    │         │         │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ        │
│    │         │         │         │
│    XXYY──────XXYY^T1_4 XXYY──────XXYY^T0_2
│    │         │         │         │
│    ×ᶠ────────×ᶠ        ×ᶠ────────×ᶠ
│    │         │         │         │
XXYY─XXYY^T1_3 XXYY──────XXYY^T0_4 │
│    │         │         │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ        │
│    │         │         │         │
│    XXYY──────XXYY^T0_3 XXYY──────XXYY^T2_4
│    │         │         │         │
│    ×ᶠ────────×ᶠ        ×ᶠ────────×ᶠ
│    │         │         │         │
XXYY─XXYY^T0_1 XXYY──────XXYY^T2_3 │
│    │         │         │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ        │
│    │         │         │         │
""".strip()

    hubbard_ansatz = SwapNetworkTrotterAnsatz(hubbard_hamiltonian)
    circuit = hubbard_ansatz.circuit
    assert circuit.to_text_diagram(transpose=True).strip() == u"""
0    1         2         3      4  5      6         7
│    │         │         │      │  │      │         │
@────@^V0_1    @─────────@^V2_3 @──@^V4_5 @─────────@^V6_7
│    │         │         │      │  │      │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ     ×ᶠ─×ᶠ     ×ᶠ────────×ᶠ
│    │         │         │      │  │      │         │
│    ×ᶠ────────×ᶠ        ×ᶠ─────×ᶠ ×ᶠ─────×ᶠ        │
│    │         │         │      │  │      │         │
XXYY─XXYY^T1_3 ×ᶠ────────×ᶠ     ×ᶠ─×ᶠ     XXYY──────XXYY^T4_6
│    │         │         │      │  │      │         │
×ᶠ───×ᶠ        │         ×ᶠ─────×ᶠ │      ×ᶠ────────×ᶠ
│    │         │         │      │  │      │         │
│    XXYY──────XXYY^T1_5 │      │  XXYY───XXYY^T2_6 │
│    │         │         │      │  │      │         │
│    ×ᶠ────────×ᶠ        │      │  ×ᶠ─────×ᶠ        │
│    │         │         │      │  │      │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ     ×ᶠ─×ᶠ     ×ᶠ────────×ᶠ
│    │         │         │      │  │      │         │
│    XXYY──────XXYY^T3_7 ×ᶠ─────×ᶠ XXYY───XXYY^T0_4 │
│    │         │         │      │  │      │         │
│    ×ᶠ────────×ᶠ        │      │  ×ᶠ─────×ᶠ        │
│    │         │         │      │  │      │         │
XXYY─XXYY^T5_7 ×ᶠ────────×ᶠ     ×ᶠ─×ᶠ     XXYY──────XXYY^T0_2
│    │         │         │      │  │      │         │
×ᶠ───×ᶠ        │         ×ᶠ─────×ᶠ │      ×ᶠ────────×ᶠ
│    │         │         │      │  │      │         │
│    ×ᶠ────────×ᶠ        ×ᶠ─────×ᶠ ×ᶠ─────×ᶠ        │
│    │         │         │      │  │      │         │
│    ×ᶠ────────×ᶠ        │      │  ×ᶠ─────×ᶠ        │
│    │         │         │      │  │      │         │
XXYY─XXYY^T5_7 ×ᶠ────────×ᶠ     ×ᶠ─×ᶠ     XXYY──────XXYY^T0_2
│    │         │         │      │  │      │         │
×ᶠ───×ᶠ        │         ×ᶠ─────×ᶠ │      ×ᶠ────────×ᶠ
│    │         │         │      │  │      │         │
│    XXYY──────XXYY^T3_7 │      │  XXYY───XXYY^T0_4 │
│    │         │         │      │  │      │         │
│    ×ᶠ────────×ᶠ        │      │  ×ᶠ─────×ᶠ        │
│    │         │         │      │  │      │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ     ×ᶠ─×ᶠ     ×ᶠ────────×ᶠ
│    │         │         │      │  │      │         │
│    XXYY──────XXYY^T1_5 ×ᶠ─────×ᶠ XXYY───XXYY^T2_6 │
│    │         │         │      │  │      │         │
│    ×ᶠ────────×ᶠ        │      │  ×ᶠ─────×ᶠ        │
│    │         │         │      │  │      │         │
XXYY─XXYY^T1_3 ×ᶠ────────×ᶠ     ×ᶠ─×ᶠ     XXYY──────XXYY^T4_6
│    │         │         │      │  │      │         │
×ᶠ───×ᶠ        │         ×ᶠ─────×ᶠ │      ×ᶠ────────×ᶠ
│    │         │         │      │  │      │         │
│    ×ᶠ────────×ᶠ        │      │  ×ᶠ─────×ᶠ        │
│    │         │         │      │  │      │         │
@────@^V0_1    @─────────@^V2_3 @──@^V4_5 @─────────@^V6_7
│    │         │         │      │  │      │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ     ×ᶠ─×ᶠ     ×ᶠ────────×ᶠ
│    │         │         │      │  │      │         │
""".strip()

    hubbard_ansatz_with_z = SwapNetworkTrotterAnsatz(hubbard_hamiltonian,
                                                     include_all_z=True)
    circuit = hubbard_ansatz_with_z.circuit
    assert circuit.to_text_diagram(transpose=True).strip() == u"""
0    1         2         3      4    5      6         7
│    │         │         │      │    │      │         │
@────@^V0_1    @─────────@^V2_3 @────@^V4_5 @─────────@^V6_7
│    │         │         │      │    │      │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ     ×ᶠ───×ᶠ     ×ᶠ────────×ᶠ
│    │         │         │      │    │      │         │
│    ×ᶠ────────×ᶠ        ×ᶠ─────×ᶠ   ×ᶠ─────×ᶠ        │
│    │         │         │      │    │      │         │
XXYY─XXYY^T1_3 ×ᶠ────────×ᶠ     ×ᶠ───×ᶠ     XXYY──────XXYY^T4_6
│    │         │         │      │    │      │         │
×ᶠ───×ᶠ        │         ×ᶠ─────×ᶠ   │      ×ᶠ────────×ᶠ
│    │         │         │      │    │      │         │
│    XXYY──────XXYY^T1_5 │      │    XXYY───XXYY^T2_6 │
│    │         │         │      │    │      │         │
│    ×ᶠ────────×ᶠ        │      │    ×ᶠ─────×ᶠ        │
│    │         │         │      │    │      │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ     ×ᶠ───×ᶠ     ×ᶠ────────×ᶠ
│    │         │         │      │    │      │         │
│    XXYY──────XXYY^T3_7 ×ᶠ─────×ᶠ   XXYY───XXYY^T0_4 │
│    │         │         │      │    │      │         │
│    ×ᶠ────────×ᶠ        │      │    ×ᶠ─────×ᶠ        │
│    │         │         │      │    │      │         │
XXYY─XXYY^T5_7 ×ᶠ────────×ᶠ     ×ᶠ───×ᶠ     XXYY──────XXYY^T0_2
│    │         │         │      │    │      │         │
×ᶠ───×ᶠ        │         ×ᶠ─────×ᶠ   │      ×ᶠ────────×ᶠ
│    │         │         │      │    │      │         │
Z^U7 ×ᶠ────────×ᶠ        Z^U4   Z^U3 ×ᶠ─────×ᶠ        Z^U0
│    │         │         │      │    │      │         │
│    Z^U6      Z^U5      ×ᶠ─────×ᶠ   Z^U2   Z^U1      │
│    │         │         │      │    │      │         │
│    ×ᶠ────────×ᶠ        │      │    ×ᶠ─────×ᶠ        │
│    │         │         │      │    │      │         │
XXYY─XXYY^T5_7 ×ᶠ────────×ᶠ     ×ᶠ───×ᶠ     XXYY──────XXYY^T0_2
│    │         │         │      │    │      │         │
×ᶠ───×ᶠ        │         ×ᶠ─────×ᶠ   │      ×ᶠ────────×ᶠ
│    │         │         │      │    │      │         │
│    XXYY──────XXYY^T3_7 │      │    XXYY───XXYY^T0_4 │
│    │         │         │      │    │      │         │
│    ×ᶠ────────×ᶠ        │      │    ×ᶠ─────×ᶠ        │
│    │         │         │      │    │      │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ     ×ᶠ───×ᶠ     ×ᶠ────────×ᶠ
│    │         │         │      │    │      │         │
│    XXYY──────XXYY^T1_5 ×ᶠ─────×ᶠ   XXYY───XXYY^T2_6 │
│    │         │         │      │    │      │         │
│    ×ᶠ────────×ᶠ        │      │    ×ᶠ─────×ᶠ        │
│    │         │         │      │    │      │         │
XXYY─XXYY^T1_3 ×ᶠ────────×ᶠ     ×ᶠ───×ᶠ     XXYY──────XXYY^T4_6
│    │         │         │      │    │      │         │
×ᶠ───×ᶠ        │         ×ᶠ─────×ᶠ   │      ×ᶠ────────×ᶠ
│    │         │         │      │    │      │         │
│    ×ᶠ────────×ᶠ        │      │    ×ᶠ─────×ᶠ        │
│    │         │         │      │    │      │         │
@────@^V0_1    @─────────@^V2_3 @────@^V4_5 @─────────@^V6_7
│    │         │         │      │    │      │         │
×ᶠ───×ᶠ        ×ᶠ────────×ᶠ     ×ᶠ───×ᶠ     ×ᶠ────────×ᶠ
│    │         │         │      │    │      │         │
""".strip()


def test_swap_network_trotter_ansatz_default_initial_params_length():

    ansatz = SwapNetworkTrotterAnsatz(hubbard_hamiltonian,
                                      include_all_yxxy=True,
                                      include_all_z=True)
    assert len(ansatz.default_initial_params()) == len(ansatz.params)
