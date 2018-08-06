from utility import float_to_str

class TEST:
    def __init__(self):
        self.file_name = {}
        self.file_name['tsne']="hi"


a = TEST()
print(a.__dict__['file_name']['tsne'])