#!/usr/bin/env python3
import random as rand

import click
import os

import lztools.Data.Images
from lztools.Bash import run_command
from lztools.Data import Text
from lztools.Data.Text import get_random_word, search_words

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

colorizations = ['none', 'rainbow', 'altbow', 'metal']

def try_read_input(input):
    try:
        return "\n".join(input.readlines())[:-1]
    except:
        return input

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """A collection of python tools and bash commands by laz aka nea"""

@main.command(context_settings=CONTEXT_SETTINGS)
@click.argument("term", default="")
@click.option('-t', '--type', type=click.Choice(['words', 'images']))
@click.option("-s", "--strict", is_flag=True, default=False)
@click.option("-m", "--max-images", default=1, type=click.IntRange(1, 500))
def search(term, type, strict, max_images):
    if type == "words":
        res = search_words(term, strict=strict)
        print(res)
    elif type == "images":
        res = lztools.Data.Images.search(term, count=max_images)
        for x in res:
            print(x)

@main.command(context_settings=CONTEXT_SETTINGS)
@click.option('-t', '--type', type=click.Choice(['words', 'images', 'colorization']), default='images')
@click.option("-c", "--count", default=1)
@click.option("-nn", "--not-nocolor", is_flag=True, default=False)
@click.argument("input", default=click.get_text_stream('stdin'))
def random(type, count, not_nocolor, input):
    if type == "images":
        res = lztools.Data.Images.get_random_image(count=count)
        for x in res:
            print(x)
    elif type == "words":
        for _ in range(count):
            print(get_random_word())
    elif type == "colorization":
        choices = colorizations
        input = try_read_input(input)
        if not_nocolor:
            choices = colorizations[1:]
        color(input, rand.choice(choices), not_nocolor=not_nocolor)

@main.command(context_settings=CONTEXT_SETTINGS)
@click.argument("input", nargs=-1)
@click.option("-d", "--delimiter", nargs=1)
def split(input, delimiter):
    i = str.join("\n", input).strip()
    if delimiter:
        i = i.split(delimiter)
    else:
        i = i.splitlines()
    for x in i:
        print(x)

@main.command(context_settings=CONTEXT_SETTINGS)
@click.argument("Regex")
@click.argument("Text", default=click.get_text_stream('stdin'))
@click.option("-s", "--single-result", is_flag=True, default=False)
def regex(regex, text, single_result):
    input = try_read_input(text)
    print(input, regex)
    if not single_result:
        for x in Text.regex(regex, input, only_first=single_result, suppress=True):
            print(x)
    else:
        print(Text.regex(regex, input, only_first=single_result, suppress=True))

# @main.command(context_settings=CONTEXT_SETTINGS)
# @click.option("-r", "--random", "operation", default=False, flag_value="random")
# @click.option("-s", "--strict", "operation", default=False, flag_value="strict")
# @click.option("-d", "--division", "operation", default=False, flag_value="division")
# @click.option("-fr", "--find-regex", "operation", default=False, flag_value="regex")
# @click.option("-f", "--find", "operation", default=True, flag_value="search")
# @click.argument("search", nargs=-1)
# def text(operation, search):
#     print(operation, search)
#     exit()
#     """Get or generate text"""
#     if operation == "random":
#         pass
#     elif operation == "strict":
#         pass
#     elif operation == "division":
#         pass
#     elif operation == "regex":
#         pass
#     elif operation == "search":
#         ss = search.split(search)
#         for part in ss:
#             if part is not None and part != "":
#                 print(part)
#     elif operation == "random" and search == "":
#     else:
#         res = search_words(search, strict=strict)
#         if random:
#             print(rand.choice(list(res)))
#         else:
#             for w in res:
#                 print(w)

# @main.command(context_settings=CONTEXT_SETTINGS)
# @click.argument("PATH")
# @click.option("-c/-m", "--color/--monochrome", default=False)
# @click.option("-w", "--width", default=100, type=click.IntRange(1, 500))
# @click.option("-i", "--invert", is_flag=True, default=False)
# def art(path, color, width, invert):
#     """fun"""
#     args = ["--width", str(width), path]
#     if color:
#         args.append("-c")
#     if invert:
#         args.append("-i")
#     command = ["asciiart", *args]
#     print("Command: {}".format(command))
#     print(subprocess.check_call(command))

@main.command(context_settings=CONTEXT_SETTINGS)
@click.argument("input")
@click.option('-t', '--type', type=click.Choice(colorizations))
@click.option("-nn", "--not-nocolor", is_flag=True, default=False)
def colorize(input, type, not_nocolor):
    color(input, type, not_nocolor)

def color(input, type, not_nocolor):
    if type == 'none':
        print(input)
    elif type == 'rainbow':
        print(run_command("toilet", "-f", "term", "--gay", input))
    elif type == 'altbow':
        os.system("echo \"{}\" | lolcat".format(input))

    elif type == 'metal':
        print(run_command("toilet", "-f", "term", "--metal", input))


if __name__ == '__main__':
    main()









# @main.command(context_settings=CONTEXT_SETTINGS)
# @click.option('--data-type', type=click.Choice(['picture', 'text']), default='picture', help="The data type to work with")
# def data(data_type):
#     """Get or generate data"""
#     if data_type == 'picture':
#         print("pic {}".format(data_type))
#     elif data_type == 'text':
#         print("text {}".format(data_type))
#     else:
#         print("Invalid argument (--data-type = {})".format(data_type))