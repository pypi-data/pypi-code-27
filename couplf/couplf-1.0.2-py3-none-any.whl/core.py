# -*- coding: utf-8 -*-
"""The core module"""
import math
import multiprocessing

from PIL import Image
from PIL import ImageDraw

from couplf import util

_WHITE = 255

def small_enough_to_fit(txt_pieces, max_height=992, max_width=1469):
    required_heights = [
        util.calculate_needed_height(piece, max_width=max_width)
        for piece in txt_pieces
    ]

    total_needed_height = sum(required_heights)

    return total_needed_height <= max_height

def create_text_bitmap(bitmap_canvas, txt_pieces):
    return _draw_text(bitmap_canvas, txt_pieces)

def create_canvas(mode, size, color):
    return Image.new(mode, size, color)

def maybe_alter_boxes(txt_pieces_dict):
    txt_bitmap_pieces = ['title', 'description', 'legal', 'expiration', 'expiration_date']

    result = []
    necessary_top_of_next = None

    for p in txt_bitmap_pieces:
        r, necessary_top_of_next = util.maybe_alter(txt_pieces_dict[p], necessary_top_of_next)
        result.append(r)

    return result

def create_corners(img, radius, **kwargs):
    """Draw a rounded rectangle"""
    width, height = img.size

    if kwargs['top']:
        corner = util.round_corner(radius, 'white')
        img.paste(corner, (0, 0))
        img.paste(corner.rotate(270), (width - radius, 0)) # Rotate the corner and paste it
    else:
        corner = util.round_corner(radius, 'white')
        img.paste(corner.rotate(90), (0, height - radius))
        img.paste(corner.rotate(180), (width - radius, height - radius))
    return img

def _draw_text_on_bitmap(draw, spec):
    (lines, text, box, font, font_size, word_spacing, line_spacing, color) = spec
    line_height = font.getsize('hg')[1]

    x = box[0]
    y = box[1]

    for line in lines:
        draw.text((x, y), line, fill=color, font=font)
        y = y + line_height

def _draw_text(page, txt_pieces):
    specs = [util.parse_page_setting(piece) for piece in txt_pieces]
    draw = ImageDraw.Draw(page)

    for spec in specs:
        _draw_text_on_bitmap(draw, spec)

    return page
