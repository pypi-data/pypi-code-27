#!/usr/bin/env python3
import argparse
from functools import partial
from types import GeneratorType

import flickrapi

def auth():
    return flickrapi.FlickrAPI("2a41e37e58cd08c0dbd5af131441dca0", "72c6a92f49f48f9e", format="parsed-json")

def add_total(img):
    img["total"] = int(img["width"])+int(img["height"])
    return img

def handle_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", default=False, action='store_true', required=False)
    args = parser.parse_args()
    return args

def search(term, count=1, verbose=False):
    photos = auth().photos_search(text=term, safe_search=3, per_page=count, extras="url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o")["photos"]["photo"]
    return map(partial(get_output, verbose=verbose), photos)

def get_random_image(verbose=False, count=1):
    photos = auth().photos.getRecent(per_page=count, extras="url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o")["photos"]["photo"]
    return map(partial(get_output, verbose=verbose), photos)

def get_outputs(images, verbose):
    for x in images:
        if isinstance(x, GeneratorType):
            for y in x:
                yield get_output(y, verbose)
        else:
            yield get_output(x, verbose)

def get_output(image, verbose=False):
    if verbose:
        return u"Title: {}\nUrl: {}".format(image["title"], image["url_o"])
    else:
        try:
            return image["url_o"]
        except:
            for k in image:
                if k.startswith("url") and image[k][-6] != "_":
                    return image[k]
