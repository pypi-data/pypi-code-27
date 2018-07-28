# -*- coding: utf-8 -*-
"""The core module"""
import math
import multiprocessing

from PIL import Image
from PIL import ImageDraw

_WHITE = 255

def create_text_bitmap(bitmap_canvas, txt_pieces):
    return _draw_text(bitmap_canvas, txt_pieces)

def _maybe_resize(img, desired):
    if img.size != desired:
        new_img = img.resize(desired)
    return new_img

def _draw_text_on_bitmap(draw, spec):
    (lines, text, box, font, font_size, word_spacing, line_spacing, color) = spec
    line_height = font.getsize('hg')[1]

    x = box[0]
    y = box[1]

    for line in lines:
        draw.text((x, y), line, fill=color, font=font)
        y = y + line_height

def _draw_text(page, txt_pieces):
    specs = [_parse_page_setting(piece) for piece in txt_pieces]
    draw = ImageDraw.Draw(page)

    for spec in specs:
        _draw_text_on_bitmap(draw, spec)

    return page

def _calculate_text_lines(text, font, max_width):
    lines = []

    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0

        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines

def _parse_page_setting(page_setting):
    """A helper function of _draw_text"""
    text = page_setting['text']
    box = page_setting['box']
    font = page_setting['font']
    font_size = page_setting['font_size']
    word_spacing = page_setting['word_spacing']
    line_spacing = page_setting['line_spacing']
    color = page_setting['font_color']

    left_side, top, right_side, bottom = box

    updated_font = font.font_variant(size=font_size)

    lines = _calculate_text_lines(text, updated_font, right_side)

    return lines, text, box, updated_font, font_size, word_spacing, line_spacing, color
