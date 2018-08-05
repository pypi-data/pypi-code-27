# -*- coding: utf-8 -*-
import multiprocessing

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from couplf import core, util

__version__ = '1.0.2'

_INTERNAL_MODE = 'L'  # The mode for internal computation
_BLACK = 0

def create_mms(template):
    txt_bitmap_pieces = ['title', 'description', 'legal', 'expiration', 'expiration_date']

    if not util.required_keys_are_present(txt_bitmap_pieces, template.keys()):
        raise KeyError

    txt_pieces_dict = dict((key, value) for key, value in template.items() if key in txt_bitmap_pieces)

    if not core.small_enough_to_fit(txt_pieces_dict.values()):
        raise ValueError("Looks like all the pieces wont fit in the canvas size available.")

    bitmap = create_text_bitmap(txt_pieces_dict)
    return merge_mms_pieces(template, bitmap)

def create_text_bitmap(txt_pieces_dict):
    size = get_bitmap_size()
    canvas = core.create_canvas(_INTERNAL_MODE, size, color=_BLACK)
    txt_pieces = core.maybe_alter_boxes(txt_pieces_dict)

    return core.create_text_bitmap(bitmap_canvas=canvas, txt_pieces=txt_pieces)

def merge_mms_pieces(template, bitmap):
    logo_img, logo_coords, logo_desired = get_specs(template['logo'])
    qr_img, qr_coords, qr_desired = get_specs(template['qr'])
    new_logo_img = maybe_format(logo_img, logo_desired, resize=True, corners=False)
    new_qr_img = maybe_format(qr_img, qr_desired, resize=True, corners=True)
    bg_img, _, _ = get_specs(template['background'])
    bg_bitmap_merged = add_text_to_bg(bg_img, bitmap)
    deal_img = put_img_on_top(bg_bitmap_merged, new_logo_img, coords=logo_coords)
    return put_img_on_top(deal_img, new_qr_img, coords=qr_coords)

def maybe_format(img, desired, **kwargs):
    if kwargs['resize'] and kwargs['corners']:
        updated_img = _maybe_resize(img, desired)
        img_t = core.create_corners(updated_img, 20, top=True)
        img_t = core.create_corners(img_t, 20, top=False)

        return img_t

    elif kwargs['corners']:
        img_t = core.create_corners(img, 20, top=True)
        img_t = core.create_corners(img_t, 20, top=False)

        return img_t

    elif kwargs['resize']:
        updated_img = _maybe_resize(img, desired)
        return updated_img

    else:
        return img

def get_bitmap_size():
    return (2048,2880)

def _maybe_resize(img, desired):
    if img.size != desired:
        new_img = img.resize(desired)
    return new_img

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

if __name__ == '__main__':
    template = {
        'background': {
            'image': Image.open("/Users/danielconger/Desktop/coup/coup-couplf/tests/data/images/coup-template.png"),
            'box':(0,0,2048,2880)
        },
        'logo': {
            'image': Image.open("/Users/danielconger/Desktop/coup/coup-couplf/tests/data/images/pdq_logo.png"),
            'box':(241, 217, 691, 274)
        },
        'qr': {
            'image': Image.open("/Users/danielconger/Desktop/coup/coup-couplf/tests/data/images/qrcode.png"),
            'box':(627, 1703, 805, 775)
        },
        'title': {
            'text':'Buy one get one free. These will go fast, so don\'t delay!',
            'box':(241, 593, 1469, 190),
            'font': ImageFont.truetype("/Users/danielconger/Desktop/coup/coup-couplf/tests/data/fonts/GT-Walsheim-Bold.otf"),
            'font_size':140,
            'line_spacing':40,
            'word_spacing':10,
            'font_color':'rgb(193,193,191)'
        },
        'description': {
            'text':'Tender and Nugget Platters. Hurry! These will fly!',
            'box':(241, 788, 1469, 203),
            'font': ImageFont.truetype("/Users/danielconger/Desktop/coup/coup-couplf/tests/data/fonts/GT-Walsheim-Medium.otf"),
            'font_size':100,
            'line_spacing':30,
            'word_spacing':10,
            'font_color':'rgb(128, 128, 128)'
        },
        'legal': {
            'text':'Valid through 6/21/18. $10 minimum purchase required.',
            'box':(241, 971, 1469, 324),
            'font': ImageFont.truetype("/Users/danielconger/Desktop/coup/coup-couplf/tests/data/fonts/GT-Walsheim-Light.otf"),
            'font_size':58,
            'line_spacing':80,
            'word_spacing':10,
            'font_color':'rgb(95, 95, 95)'
        },
        'expiration': {
            'text': 'EXPIRES',
            'box': (241, 1304, 1469, 136),
            'font': ImageFont.truetype("/Users/danielconger/Desktop/coup/coup-couplf/tests/data/fonts/GT-Walsheim-Bold.otf"),
            'font_size': 70,
            'line_spacing':20,
            'word_spacing':10,
            'font_color':'rgb(193,193,175)'
        },
        'expiration_date': {
            'text': '9-16-2018',
            'box': (241, 1440, 1469, 139),
            'font': ImageFont.truetype("/Users/danielconger/Desktop/coup/coup-couplf/tests/data/fonts/GT-Walsheim-Medium.otf"),
            'font_size': 100,
            'line_spacing':0,
            'word_spacing':10,
            'font_color':'rgb(128, 128, 128)'
        }
    }

    img = create_mms(template)
    img.show()
