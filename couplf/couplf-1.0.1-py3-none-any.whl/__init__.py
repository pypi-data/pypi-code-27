# -*- coding: utf-8 -*-
import multiprocessing

from PIL import Image
from PIL import ImageDraw
from couplf import _core

__version__ = '1.0.1'

_INTERNAL_MODE = 'L'  # The mode for internal computation
_BLACK = 0

"""
template = {
    'background': {
        'image': image.open('./tests/data/backgrounds/coup.png'),
        'box':(0,0,2048,2880)
    },
    'logo': {
        'image': image.open('./tests/data/backgrounds/logo.png'),
        'box':(241, 217, 691, 274)
    },
    'qr': {
        'image': image.open('./tests/data/backgrounds/qrcode.png'),
        'box':(627, 1703, 805, 775)
    },
    'title': {
        'text':'Buy one get one free',
        'box':(241, 593, 1469, 190),
        'font': image_font.truetype('./tests/data/fonts/OverpassMono-Bold.ttf'),
        'font_size':71,
        'line_spacing':10,
        'word_spacing':10,
        'color':'rgb(0, 0, 0)'
    },
    'description': {
        'text':'Tender and Nugget Platters',
        'box':(241, 788, 1469, 203),
        'font': image_font.truetype('./tests/data/fonts/OverpassMono-Bold.ttf'),
        'font_size':55,
        'line_spacing':10,
        'word_spacing':10,
        'color':'rgb(0, 0, 0)'
    },
    'legal': {
        'text':'Valid through 6/21/18. $10 minimum purchase required, based on the transaction total prior to taxes and after discounts are applied. Limit one coupon per transaction.',
        'box':(241, 971, 1469, 324),
        'font': image_font.truetype('./tests/data/fonts/OverpassMono-Bold.ttf'),
        'font_size':21,
        'line_spacing':10,
        'word_spacing':10,
        'color':'rgb(0, 0, 0)'
    }
}
"""
def create_mms(template):
    txt_bitmap_pieces = ['title', 'description', 'legal', 'expiration', 'expiration_date']
    txt_pieces = [template[piece] for piece in txt_bitmap_pieces]
    bitmap = create_text_bitmap(txt_pieces)
    return merge_mms_pieces(template, bitmap)

def round_corner(radius, fill):
    """Draw a round corner"""
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    # (x0, y0, x1, y1), starting_angle (measured from 3 oclock increasing clockwise), end_angle, fill
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
    return corner

def create_corners(img, radius, **kwargs):
    """Draw a rounded rectangle"""
    width, height = img.size

    if kwargs['top']:
        corner = round_corner(radius, 'white')
        img.paste(corner, (0, 0))
        img.paste(corner.rotate(270), (width - radius, 0)) # Rotate the corner and paste it
    else:
        corner = round_corner(radius, 'white')
        img.paste(corner.rotate(90), (0, height - radius))
        img.paste(corner.rotate(180), (width - radius, height - radius))
    return img

def _maybe_resize(img, desired):
    if img.size != desired:
        new_img = img.resize(desired)
    return new_img

def maybe_format(img, desired, **kwargs):
    if kwargs['resize'] and kwargs['corners']:
        updated_img = _maybe_resize(img, desired)
        img_t = create_corners(updated_img, 20, top=True)
        img_t = create_corners(img_t, 20, top=False)

        return img_t

    elif kwargs['corners']:
        img_t = create_corners(img, 20, top=True)
        img_t = create_corners(img_t, 20, top=False)

        return img_t

    elif kwargs['resize']:
        updated_img = _maybe_resize(img, desired)
        return updated_img

    else:
        return img

def add_text_to_bg(bg_img, text_page):
    res = bg_img.copy()
    draw = ImageDraw.Draw(res)
    draw.bitmap(xy=(0, 0), bitmap=text_page, fill='rgb(0, 0, 0)')
    return res

def get_specs(img_specs):
    (x, y, desired_width, desired_height) = img_specs['box']
    return img_specs['image'], (x, y), (desired_width, desired_height)

def put_img_on_top(img, on_top_img, coords=(0, 0)):
    img.paste(on_top_img, box=coords, mask=on_top_img)
    return img

def merge_mms_pieces(template, bitmap):
    logo_img, logo_coords, logo_desired = get_specs(template['logo'])
    qr_img, qr_coords, qr_desired = get_specs(template['qr'])
    new_logo_img = maybe_format(logo_img, logo_desired, resize=True, corners=False)
    new_qr_img = maybe_format(qr_img, qr_desired, resize=True, corners=True)
    bg_img, _, _ = get_specs(template['background'])
    bg_bitmap_merged = add_text_to_bg(bg_img, bitmap)
    deal_img = put_img_on_top(bg_bitmap_merged, new_logo_img, coords=logo_coords)
    return put_img_on_top(deal_img, new_qr_img, coords=qr_coords)

def get_bitmap_size():
    return (2048,2880)

def create_canvas(mode, size, color):
    return Image.new(mode, size, color)

def create_text_bitmap(txt_pieces):
    size = get_bitmap_size()
    canvas = create_canvas(_INTERNAL_MODE, size, color=_BLACK)

    return _core.create_text_bitmap(bitmap_canvas=canvas, txt_pieces=txt_pieces)
