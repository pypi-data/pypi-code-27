# -*- coding: utf-8 -*-
# Copyright (c) 2015, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.


def get_color_names():
    """Get the known color names

    Returns
    -------
    names : list
        List of color names known by Vispy.
    """
    names = list(_color_dict.keys())
    names.sort()
    return names


def get_color_dict():
    """Get the known colors

    Returns
    -------
    color_dict : dict
        Dict of colors known by Vispy {name: #rgb}.
    """
    return _color_dict.copy()


# This is used by color functions to translate user strings to colors
# For now, this is web colors, and all in hex. It will take some simple
# but annoying refactoring to deal with non-hex entries if we want them.

# Add the CSS colors, courtesy MIT-licensed code from Dave Eddy:
# github.com/bahamas10/css-color-names/blob/master/css-color-names.json

_color_dict = {
    "k": '#000000',
    "w": '#FFFFFF',
    "r": '#FF0000',
    "g": '#00FF00',
    "b": '#0000FF',
    "y": '#FFFF00',
    "m": '#FF00FF',
    "c": '#00FFFF',
    "aqua": "#00ffff",
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "black": "#000000",
    "blue": "#0000ff",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgreen": "#006400",
    "darkturquoise": "#00ced1",
    "deepskyblue": "#00bfff",
    "green": "#008000",
    "lime": "#00ff00",
    "mediumblue": "#0000cd",
    "mediumspringgreen": "#00fa9a",
    "navy": "#000080",
    "springgreen": "#00ff7f",
    "teal": "#008080",
    "midnightblue": "#191970",
    "dodgerblue": "#1e90ff",
    "lightseagreen": "#20b2aa",
    "forestgreen": "#228b22",
    "seagreen": "#2e8b57",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "limegreen": "#32cd32",
    "mediumseagreen": "#3cb371",
    "turquoise": "#40e0d0",
    "royalblue": "#4169e1",
    "steelblue": "#4682b4",
    "darkslateblue": "#483d8b",
    "mediumturquoise": "#48d1cc",
    "indigo": "#4b0082",
    "darkolivegreen": "#556b2f",
    "cadetblue": "#5f9ea0",
    "cornflowerblue": "#6495ed",
    "mediumaquamarine": "#66cdaa",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "slateblue": "#6a5acd",
    "olivedrab": "#6b8e23",
    "slategray": "#708090",
    "slategrey": "#708090",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "mediumslateblue": "#7b68ee",
    "lawngreen": "#7cfc00",
    "aquamarine": "#7fffd4",
    "chartreuse": "#7fff00",
    "gray": "#808080",
    "grey": "#808080",
    "maroon": "#800000",
    "olive": "#808000",
    "purple": "#800080",
    "lightskyblue": "#87cefa",
    "skyblue": "#87ceeb",
    "blueviolet": "#8a2be2",
    "darkmagenta": "#8b008b",
    "darkred": "#8b0000",
    "saddlebrown": "#8b4513",
    "darkseagreen": "#8fbc8f",
    "lightgreen": "#90ee90",
    "mediumpurple": "#9370db",
    "darkviolet": "#9400d3",
    "palegreen": "#98fb98",
    "darkorchid": "#9932cc",
    "yellowgreen": "#9acd32",
    "sienna": "#a0522d",
    "brown": "#a52a2a",
    "darkgray": "#a9a9a9",
    "darkgrey": "#a9a9a9",
    "greenyellow": "#adff2f",
    "lightblue": "#add8e6",
    "paleturquoise": "#afeeee",
    "lightsteelblue": "#b0c4de",
    "powderblue": "#b0e0e6",
    "firebrick": "#b22222",
    "darkgoldenrod": "#b8860b",
    "mediumorchid": "#ba55d3",
    "rosybrown": "#bc8f8f",
    "darkkhaki": "#bdb76b",
    "silver": "#c0c0c0",
    "mediumvioletred": "#c71585",
    "indianred": "#cd5c5c",
    "peru": "#cd853f",
    "chocolate": "#d2691e",
    "tan": "#d2b48c",
    "lightgray": "#d3d3d3",
    "lightgrey": "#d3d3d3",
    "thistle": "#d8bfd8",
    "goldenrod": "#daa520",
    "orchid": "#da70d6",
    "palevioletred": "#db7093",
    "crimson": "#dc143c",
    "gainsboro": "#dcdcdc",
    "plum": "#dda0dd",
    "burlywood": "#deb887",
    "lightcyan": "#e0ffff",
    "lavender": "#e6e6fa",
    "darksalmon": "#e9967a",
    "palegoldenrod": "#eee8aa",
    "violet": "#ee82ee",
    "azure": "#f0ffff",
    "honeydew": "#f0fff0",
    "khaki": "#f0e68c",
    "lightcoral": "#f08080",
    "sandybrown": "#f4a460",
    "beige": "#f5f5dc",
    "mintcream": "#f5fffa",
    "wheat": "#f5deb3",
    "whitesmoke": "#f5f5f5",
    "ghostwhite": "#f8f8ff",
    "lightgoldenrodyellow": "#fafad2",
    "linen": "#faf0e6",
    "salmon": "#fa8072",
    "oldlace": "#fdf5e6",
    "bisque": "#ffe4c4",
    "blanchedalmond": "#ffebcd",
    "coral": "#ff7f50",
    "cornsilk": "#fff8dc",
    "darkorange": "#ff8c00",
    "deeppink": "#ff1493",
    "floralwhite": "#fffaf0",
    "fuchsia": "#ff00ff",
    "gold": "#ffd700",
    "hotpink": "#ff69b4",
    "ivory": "#fffff0",
    "lavenderblush": "#fff0f5",
    "lemonchiffon": "#fffacd",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightyellow": "#ffffe0",
    "magenta": "#ff00ff",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "pink": "#ffc0cb",
    "red": "#ff0000",
    "seashell": "#fff5ee",
    "snow": "#fffafa",
    "tomato": "#ff6347",
    "white": "#ffffff",
    "yellow": "#ffff00",
}
