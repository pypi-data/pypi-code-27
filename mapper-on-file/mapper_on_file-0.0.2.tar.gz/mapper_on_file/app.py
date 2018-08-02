import demjson
from codegenhelper import debug
from deep_mapper import process_mapping

def mapping(map_file, json_data, root_path = "/"):
    return process_mapping(json_data, debug(demjson.decode_file(map_file), "mapper:"), root_path)
