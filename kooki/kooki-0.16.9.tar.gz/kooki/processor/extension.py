import os, empy
import pretty_output

from kooki.tools import get_front_matter, read_file

from .common import apply_template
from .metadata import Metadata
from .renderer import render
from .exception import ErrorEvaluatingExpression


def load_extensions(document, template_extension):
    loader = ExtensionLoader(document, template_extension)
    loader.load()
    return loader.extensions


class ExtensionLoader():

    def __init__(self, document, template_extension):
        self.document = document
        self.template_extension = template_extension
        self.extensions = Metadata()

    def load(self):
        self.load_jars()
        self.load_locals()

    def load_locals(self):
        path = os.path.join(os.getcwd(), self.document.context)
        self.load_directory(path)

    def load_jars(self):
        for path in self.document.jars:
            self.load_directory(path)

    def load_directory(self, directory, prefix=[]):
        for element in os.listdir(directory):
            path = os.path.join(directory, element)
            if os.path.isdir(path):
                self.load_directory(path, prefix=[*prefix, element])

            elif os.path.isfile(path):
                root, ext = os.path.splitext(element)
                if ext in ['.md', self.template_extension]:
                    self.add(root, ext, path, prefix)

    def add(self, name, ext, path, prefix):
        tmp = self.extensions
        for prefix_part in prefix:
            if prefix_part not in tmp:
                tmp[prefix_part] = Metadata()
            tmp = tmp[prefix_part]
            if isinstance(tmp, Extension):
                pretty_output.error(tmp.path)
        tmp[name] = self.create(name, path, ext)

    def create(self, name, file_full_path, ext):
        extension = Extension(self.document, name, file_full_path, ext)
        return extension


class RawExtension():

    level = 0

    def __init__(self, document, template_extension, file_content):
        self.document = document
        self.name = 'direct load'
        self.path = 'direct load'
        self.template_extension = template_extension
        self.front_matter, self.content = get_front_matter(file_content)

    def __call__(self, *args, **kwargs):
        try:
            metadata = Metadata()
            metadata.update(self.front_matter)
            metadata.update(self.document.metadata)
            new_args = {}
            for index, arg in enumerate(args):
                new_args['arg{}'.format(index)] = arg
            metadata.update(**new_args)
            metadata.update(**kwargs)

            content = self.content

            pretty_output.debug_on()
            if Extension.level == 0:
                pretty_output.colored(self.name, 'white', 'on_yellow')
            else:
                message = ''
                for i in range(0, self.level-1):
                    message += '│   '
                message += '├'
                message += '─' * 2
                message += ' '
                pretty_output.colored(message, 'white', 'on_yellow', end='')
                pretty_output.colored(self.name, 'white', 'on_yellow')
            Extension.level += 1
            char = '└'
            pretty_output.debug_off()

            caller = Caller()
            caller.update(metadata)
            content = apply_interpreter(content, caller, prefix='@')

            if self.template_extension == '.md':
                content = render(content, metadata)

            for placeholder_key, placeholder_value in Element.placeholders.items():
                content = content.replace(placeholder_key, placeholder_value)

            Extension.level -= 1

            return content

        except ErrorEvaluatingExpression as e:
            e.add_path(self.path)
            raise e


class Extension(RawExtension):

    def __init__(self, document, name, path, template_extension):
        self.document = document
        self.name = name
        self.path = path
        self.template_extension = template_extension
        file_content = read_file(path)
        self.front_matter, self.content = get_front_matter(file_content)


import random, string

class Element():

    placeholders = {}

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_var_name(self):
        name = ''.join(random.choice(string.ascii_uppercase) for _ in range(25))
        while name in Element.placeholders:
            name = ''.join(random.choice(string.ascii_uppercase) for _ in range(25))
        return name

    def __repr__(self):
        name = self.get_var_name()
        Element.placeholders[name] = str(self.value)
        return '{}'.format(name)

    def __call__(self, *args, **kwargs):
        name = self.get_var_name()
        Element.placeholders[name] = self.value(*args, **kwargs)
        return '{}'.format(name)


def is_builtin_class_instance(obj):
    return obj.__class__.__module__ == '__builtin__'


class Caller(Metadata):

    def __getitem__(self, key):
        self.update(__builtins__)
        self.update(locals()['self'])
        value = self.get(key)

        if is_builtin_class_instance(value):
            return type('', (type(value), Element), {})(key, value)

        elif isinstance(value, Extension):
            return type('', (Element,), {})(key, value)

        elif isinstance(value, Metadata):
            caller = Caller()
            caller.update(value)
            return caller

        else:
            return value


def apply_interpreter(content, metadata, prefix):
    interpreter = empy.Interpreter()
    interpreter.setPrefix(prefix)
    result = interpreter.expand(content, metadata)
    return result