#!/usr/bin/env python
import requests
import json
from os import path
from functools import partial
from collections import defaultdict

from dinner_time.constants import (
    RECIPES_FN,
    CFG_FN,
    GOOGLE_SHEETS_ENDPOINT,
    TAG_ALL
)

from dinner_time.util import (
    nonempty
)


def get_sheet_key():
    with open(CFG_FN, 'r') as fp:
        cfg = json.load(fp)
        sheet_key = cfg["sheet_key"]
    return sheet_key


def get_recipes_from_web():
    export_params = "export?format=csv&id=0"
    export_url = "{endpoint}/{key}/{params}".format(
        endpoint=GOOGLE_SHEETS_ENDPOINT, key=get_sheet_key(), params=export_params
    )

    response = requests.get(export_url)
    if response.status_code != 200:
        raise Exception("Request to {} received a status code of {}.".format(export_url, response.status_code))
    return response.text


def parse_line(line):
    tokens = filter(nonempty, line.strip().split(','))
    return tokens[0], tokens[1:]


def parse_recipe(mapping, line):
    recipe, tags = parse_line(line)
    for tag in tags:
        mapping[tag].add(recipe)
        mapping[TAG_ALL].add(recipe)


def get_recipes(update=False):
    # if needed, update the recipes first
    if update or not path.exists(RECIPES_FN):
        recipes = update_recipes(get_recipes_from_web())
        persist_recipes_to_disk(recipes)
        return recipes
    return load_recipes()


def load_recipes():
    # load the recipes from disk
    with open(RECIPES_FN, 'r') as fp:
        recipes = json.load(fp)
    return recipes


def update_recipes(text):
    # parse the data into a dict of {tag: set(recipes)}
    tags_to_recipes = defaultdict(set)
    map(
        partial(parse_recipe, tags_to_recipes),
        text.split('\n')[1:]
    )

    # convert the final sets to lists for compatibility with json.dump
    return {
        tag: list(recipes)
        for tag, recipes in tags_to_recipes.items()
    }


def persist_recipes_to_disk(recipes):
    with open(RECIPES_FN, 'w') as fp:
        json.dump(recipes, fp, indent=4)
