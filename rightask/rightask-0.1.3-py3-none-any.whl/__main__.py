#!/usr/bin/env python

from rt.db import collection
from uuid import uuid4


class Main:
    def __init__(self):
        root = collection.find_one({"title": "root"})
        if root is None:
                id_ = uuid4().bytes
                collection.insert_one({"id": id_,
                                       "title": "root",
                                       "parent": None,
                                       "children": []})
                self.pointer = id_
        else:
            self.pointer = root["id"]

    def add_dir(self, name_dir):
        new_id = uuid4().bytes
        collection.update({"id": self.pointer}, {'$push': {'children': new_id}})
        collection.insert_one({"id": new_id, "title": name_dir, "parent": self.pointer, "children": []})

    def cd(self, name_dir):
        children = collection.find_one({"id": self.pointer})['children']
        if name_dir == '..':
            parent_pointer = collection.find_one({"id": self.pointer})['parent']
            if parent_pointer is not None:
                self.pointer = parent_pointer
            return
        for child in children:
            child_obj = collection.find_one({"id": child})
            if child_obj['title'] == name_dir:
                self.pointer = child_obj['id']

    def ls(self):
        children = collection.find_one({"id": self.pointer})['children']
        for child in children:
            print(f"> {collection.find_one({'id': child})['title']}")

    def delete(self, *args):
        assert len(args) == 1
        name_dir = args[0]
        print(name_dir)
        children_ids = collection.find_one({'id': self.pointer})['children']
        for child_id in children_ids:
            child = collection.find_one({'id': child_id})
            if child['title'] == name_dir:
                collection.update_one({'id': self.pointer}, {'$pull': {'children': child_id}})
                collection.delete_one({'id': child_id})
                break

    def check(self, *args):
        assert len(args) == 1
        name_dir = args[0]
        children_ids = collection.find_one({'id': self.pointer})['children']
        for child_id in children_ids:
            child = collection.find_one({'id': child_id})
            if child['title'] == name_dir:
                collection.update_one({'id': child_id}, {'$set' : {'state': 'done'}})
                break

    def reset_db(self, *args):
        assert len(args) == 0
        collection.remove({})
        self.__init__()


def main():
    m = Main()

    while 1:
        try:
            inp = input('$ ')
            functions = {
                'cd': m.cd,
                'ls': m.ls,
                'add': m.add_dir,
                'del': m.delete,
                'check': m.check,
                'reset_db': m.reset_db,
            }
            words = inp.split(" ")
            functions[words[0]](*words[1:])
        except KeyboardInterrupt:
            print("bye!")
            break

if __name__ == '__main__':
    main()
