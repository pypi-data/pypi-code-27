#!/usr/bin/env python3

import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """A collection of python tools and bash commands for manipulating text by laz aka nea"""

if __name__ == '__main__':
    main()




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