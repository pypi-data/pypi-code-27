import os
import json
from pkg_resources import resource_exists, resource_string

class FileHandler:
    def load_from_path(self, file_path):
        oc = self.output_control
        if os.path.exists(file_path):
            try:
                json_file = open(file_path, 'r', encoding='utf-8-sig')
                content = json.load(json_file)
                json_file.close()
                return content 
            except:
                oc.print(oc.COULD_NOT_LOAD, (file_path,))
        else:
            oc.print(oc.SETT_FILE_NOT_FOUND, (file_path,))

    def __init__(self, output_control):
        self.output_control = output_control

    def read_library(self, file_path):
        oc = self.output_control
        oc.print(oc.FILE_PATH, (file_path,))
        data_dicts = []
        directories = []
        for file_name in os.listdir(file_path):
            oc.print(oc.FILE_CHECK, (file_name,))
            if '.json' in file_name:
                data_dicts.append(self.load_from_path('{0}{1}'.format(file_path, file_name)))
                oc.print(oc.FILE_ADDED_COMS)
            elif '.' in file_name:
                oc.print(oc.WRONG_EXT)
            else:
                oc.print(oc.IS_DIR, (file_name,))
                directories.append(file_name)
        return (data_dicts, directories)
