import os

def get_file_content(path):
    with open(path, 'r') as f:
        return ''.join(f.readlines())

def get_folder_content(path):
    data = {}
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isdir(file_path):
            data[file_name] = get_folder_content(file_path)
        else:
            if file_name.endswith('.lua'):
                data[file_name] = get_file_content(file_path)
    return data

def get_content(path):
    return get_folder_content(path)
