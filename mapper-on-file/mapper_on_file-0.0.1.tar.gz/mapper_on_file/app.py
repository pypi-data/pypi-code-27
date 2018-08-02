import demjson
from codegenhelper import debug
from deep_mapper import process_mapping

def mapping(map_file, json_data):
    return process_mapping(json_data, debug(demjson.decode_file(map_file), "mapper:"), "/")
