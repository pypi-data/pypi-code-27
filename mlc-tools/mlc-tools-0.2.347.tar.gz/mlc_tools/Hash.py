import json
import hashlib
import os
import sys
from . import fileutils

if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle


class Hash:

    def __init__(self, root):
        self.root = root
        self.kwargs = {}
        self.configs = {}
        self.classes = {}
        self.files_md5 = {}
        self.classes_body = {}
        self.classes_for_data = {}
        self.dict = {
            'cnf': self.configs,
            'cls': self.classes,
            'fm5': self.files_md5,
            'cbd': self.classes_body,
            'cfd': self.classes_for_data
        }

    def get_md5(self, data):
        m = hashlib.md5()
        try:
            m.update(data.encode('utf-8'))
        except UnicodeDecodeError:
            m.update(data)

        return m.hexdigest()

    def is_file_changed(self, filename, filedata):
        if filename not in self.files_md5:
            return True
        return self.get_md5(filedata) != self.files_md5[filename]

    def get_hash_filename(self):
        return '{}/.mlc/{}.hash'.format(self.root, self.get_md5(json.dumps(self.kwargs)))

    def add_cls(self, config_filename, class_):
        if config_filename not in self.configs:
            self.configs[config_filename] = []
        self.configs[config_filename].append(class_)
        self.classes[class_.name] = config_filename

    def add_cls_data(self, cls):
        if cls.name not in self.classes_for_data:
            self.classes_for_data[cls.name] = cls

    def get_classes_from_file(self, filename):
        if filename not in self.configs:
            return []
        return self.configs[filename]

    def get_class_body(self, cls, postfix=''):
        name = cls.name + postfix
        if name in self.classes_body:
            return self.classes_body[name]
        return ''

    def get_classes_for_data(self):
        result = []
        for key in self.classes_for_data:
            result.append(self.classes_for_data[key])
        return result

    def fix_class_body(self, cls, body, postfix=''):
        name = cls.name + postfix
        self.classes_body[name] = body

    def fix_file(self, filename, data):
        self.files_md5[filename] = self.get_md5(data)

    def save(self):
        data = pickle.dumps(self.dict, 2)
        filename = self.get_hash_filename()
        fileutils.create_dir_for_file(filename)
        open(filename, 'wb').write(data)

    def load(self, **kwargs):
        self.kwargs = kwargs
        filename = self.get_hash_filename()
        if os.path.isfile(filename):
            fileutils.create_dir_for_file(filename)
            data = open(filename, 'rb').read()
            if data:
                self.dict = pickle.loads(data)
                self.configs = self.dict['cnf']
                self.classes = self.dict['cls']
                self.files_md5 = self.dict['fm5']
                self.classes_body = self.dict['cbd']
                self.classes_for_data = self.dict['cfd']
