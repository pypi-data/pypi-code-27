import hashlib
import importlib


def get_class_from_path(dotted_path):
    """
    Get class or function based on dotted path
    :param dotted_path: string (dotted.path.to.class.or.function)
    :return: class or function object
    """
    if not isinstance(dotted_path, str) or not '.' in dotted_path:
        raise TypeError('Probably "%s" is not a dotted path to class or function.' % dotted_path)

    path_in_list = dotted_path.split('.')
    path_to_module = '.'.join(path_in_list[:-1])
    path_to_class = path_in_list[-1]
    module_class = importlib.import_module(path_to_module)
    return getattr(module_class, path_to_class)


def md5_from_string(string):
    """
    Create md5 from string
    :param string: string
    :return: md5 string
    """
    return hashlib.md5(string.encode('utf-8')).hexdigest()
