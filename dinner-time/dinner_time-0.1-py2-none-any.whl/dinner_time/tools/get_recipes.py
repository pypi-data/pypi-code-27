#!/usr/bin/env python
from argparse import ArgumentParser

from dinner_time.recipes import get_recipes
from dinner_time.constants import TAG_ALL


def recipes_with_tags(recipes, tags):
    # if no tags are given, use the 'all' tagreturn all recipes
    if len(tags) == 0:
        tags = [TAG_ALL]

    # form a set of all the recipes which have the given tags
    matches = set()
    for tag in tags:
        tagged_recipes = recipes.get(tag)
        if tagged_recipes:
            map(matches.add, tagged_recipes)
    return list(matches)


def build_parser():
    parser = ArgumentParser()
    parser.add_argument(dest="tags", nargs="*")
    parser.add_argument("-u", "--update", action="store_true")
    return parser


def main():
    args = build_parser().parse_args()
    recipes = get_recipes(args.update)
    print recipes_with_tags(recipes, args.tags)


if __name__ == '__main__':
    main()
