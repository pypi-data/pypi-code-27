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

from __future__ import with_statement
from __future__ import absolute_import
import pytest

from cirq.circuits import TextDiagramDrawer
from cirq.testing.mock import mock


def test_draw_entries_and_lines_with_options():
    d = TextDiagramDrawer()
    d.write(0, 0, u'!')
    d.write(6, 2, u'span')
    d.horizontal_line(y=3, x1=2, x2=8)
    d.vertical_line(x=7, y1=1, y2=4)
    assert d.render().strip() == u"""
!

                 │
                 │
            span │
                 │
    ─────────────┼─
                 │
    """.strip()

    assert d.render(use_unicode_characters=False).strip() == u"""
!

                 |
                 |
            span |
                 |
    -------------+-
                 |
    """.strip()

    assert d.render(crossing_char=u'@').strip() == u"""
!

                 │
                 │
            span │
                 │
    ─────────────@─
                 │
    """.strip()

    assert d.render(horizontal_spacing=0).strip() == u"""
!

          │
          │
      span│
          │
  ────────┼
          │
    """.strip()

    assert d.render(vertical_spacing=0).strip() == u"""
!
                 │
            span │
    ─────────────┼─
    """.strip()


def test_draw_entries_and_lines_with_emphasize():
    d = TextDiagramDrawer()
    d.write(0, 0, u'!')
    d.write(6, 2, u'span')
    d.grid_line(2, 3, 8, 3, True)
    d.grid_line(7, 1, 7, 4, True)
    print d.render().strip()
    assert d.render().strip() == u"""
!

                 ┃
                 ┃
            span ┃
                 ┃
    ━━━━━━━━━━━━━━━
                 ┃
    """.strip()


def test_line_detects_horizontal():
    d = TextDiagramDrawer()
    with mock.patch.object(d, u'vertical_line') as vertical_line:
        d.grid_line(1, 2, 1, 5, True)
        vertical_line.assert_called_once_with(1, 2, 5, True)


def test_line_detects_vertical():
    d = TextDiagramDrawer()
    with mock.patch.object(d, u'horizontal_line') as horizontal_line:
        d.grid_line(2, 1, 5, 1, True)
        horizontal_line.assert_called_once_with(1, 2, 5, True)


def test_line_fails_when_not_aligned():
    d = TextDiagramDrawer()
    with pytest.raises(ValueError):
        d.grid_line(1, 2, 3, 4)