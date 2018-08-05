from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def calculate_text_lines(text, font, max_width):
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

def calculate_font_variant(font, font_size):
    return font.font_variant(size=font_size)

def calculate_needed_height(params, max_width=1469):
    updated_font = calculate_font_variant(params['font'], params['font_size']) # do we maybe need to take this down?
    lines = calculate_text_lines(params['text'], updated_font, max_width)
    font_height = updated_font.getsize(params['text'])[1]
    return font_height * len(lines)

def required_keys_are_present(required, present):
    return all([k in present for k in required])

def parse_page_setting(page_setting):
    """A helper function of _draw_text"""
    text = page_setting['text']
    box = page_setting['box']
    font = page_setting['font']
    font_size = page_setting['font_size']
    word_spacing = page_setting['word_spacing']
    line_spacing = page_setting['line_spacing']
    color = page_setting['font_color']

    left_side, top, right_side, bottom = box

    updated_font = font.font_variant(size=font_size) # do we maybe need to take this down?

    lines = calculate_text_lines(text, updated_font, right_side)

    return lines, text, box, updated_font, font_size, word_spacing, line_spacing, color

def round_corner(radius, fill):
    """Draw a round corner"""
    corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
    return corner

def get_box_piece(box, wanted='left'):
    if wanted == 'left':
        return box[0]
    elif wanted == 'top':
        return box[1]
    elif wanted == 'width':
        return box[2]
    else:
        # wanted == 'height'
        return box[3]

def alter_box(box, val, piece=''):
    l = list(box)

    if piece == 'top':
        l[1] = val
    if piece == 'height':
        l[3] = val

    return tuple(l)

def maybe_alter(ti, necessary_top=None):
    (_, top, _, height) = ti['box'] #(241, 788, 1469, 203)

    if necessary_top is None:
        necessary_top = top

    if top < necessary_top: #788 < 1004
        top = necessary_top
        ti['box'] = alter_box(ti['box'], necessary_top, piece='top')

    min_needed_height = calculate_needed_height(ti, max_width=1469) + ti['line_spacing']

    if min_needed_height > height:
        ti['box'] = alter_box(ti['box'], min_needed_height, piece='height')

    return ti, top + min_needed_height
