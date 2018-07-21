#!/usr/bin/env python
import curses

from view import screen, Pad, Menu

def init(world):
    pad = Pad(height=world.height, width=world.width)
    for y, row in enumerate(world.map):
        for x, tile in enumerate(row):
            if tile.mode:
                pad.addch(y, x, tile.vis, tile.mode)
            else:
                pad.addch(y, x, tile.vis)
    pad.refresh(0, 0, 0, 0, pad.scr_height-1, pad.scr_width-1)
