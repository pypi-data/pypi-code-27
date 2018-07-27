# -*- coding:utf-8 -*-
import sys
import re
import os
import time
import copy
import json
import platform

if sys.version[0] == '2':
    from .funclib_conf import *
else:
    from funclib.funclib_conf import *
    from functools import reduce


class FuncLib(object):
    """
    ===============================================================================
                                    Func-Lib
                    A data processing methods lib for Python(2/3)
    -------------------------------------------------------------------------------
                           Author: @CN-Tower
                        Create At: 2018-2-2
                        Update At: 2018-3-15
                          Version: 2.1.5
                           GitHub: http://github.com/CN-Tower/funclib.py
    -------------------------------------------------------------------------------
            fn.index         fn.find           fn.filter         fn.reject
            fn.reduce        fn.contains       fn.flatten        fn.uniq
            fn.pluck         fn.every          fn.some           fn.tolist
            fn.drop          fn.typeof         fn.typeval        fn.get
            fn.dump          fn.test           fn.replace        fn.iscan
            fn.log           fn.timer          fn.now            fn.clear
    ===============================================================================
    """
    
    @staticmethod
    def index(predicate, src_list):
        """ 
        ### fn.index
            Looks through the list and returns the item index. If no match is found,
            or if list is empty, -1 will be returned.
            eg:
                persons = [{"name": "Tom", "age": 12},
                    {"name": "Jerry", "age": 20},
                    {"name": "Mary", "age": 35}]
                fn.index({"name": 'Jerry'}, persons)              # => 1
                fn.index(lambda x: x['name'] == 'Mary', persons)  # => 2
        """
        tmp_list = FuncLib.__listlize(src_list)
        if tmp_list and FuncLib.typeof(tmp_list, 'lst'):
            if predicate in tmp_list:
                return tmp_list.index(predicate)
            elif isinstance(predicate, dict):
                for i in range(0, len(tmp_list)):
                    tmp_bool = True
                    for key in predicate:
                        if key not in tmp_list[i] or predicate[key] != tmp_list[i][key]:
                            tmp_bool = False
                            break
                    if tmp_bool:
                        return i
                return -1
            elif FuncLib.typeof(predicate, 'fun'):
                for i in range(0, len(tmp_list)):
                    if predicate(tmp_list[i]):
                        return i
            return -1
        return -1

    @staticmethod
    def find(predicate, src_list):
        """
        ### fn.find
            Looks through each value in the list, returning the first one that passes
            a truth test (predicate), or None.If no value passes the test the function
            returns as soon as it finds an acceptable element, and doesn't traverse
            the entire list.
            eg:
                persons = [{"name": "Tom", "age": 12},
                    {"name": "Jerry", "age": 20},
                    {"name": "Mary", "age": 35}]
                Jerry = fn.find({"name": 'Jerry'}, persons)
                Mary  = fn.find(lambda x: x['name'] == 'Mary', persons)
                print(Jerry)  # => {'age': 20, 'name': 'Jerry'}
                print(Mary)   # => {'age': 35, 'name': 'Mary'}
        """
        idx = FuncLib.index(predicate, src_list)
        if idx != -1:
            return src_list[idx]
        return None

    @staticmethod
    def filter(predicate, src_list):
        """
        ### fn.filter
            Looks through each value in the list, returning an array of all the values
            that pass a truth test (predicate).
            eg:
                persons = [{"name": "Tom", "age": 20},
                            {"name": "Jerry", "age": 20},
                            {"name": "Jerry", "age": 35}]
                Jerry = fn.filter({"age": 20}, persons)
                Mary = fn.filter(lambda x: x['name'] == 'Jerry', persons)
                print(Jerry)  # => [{'age': 20, 'name': 'Tom'},
                                    {'age': 20, 'name': 'Jerry'}]
                print(Mary)   # => [{'age': 20, 'name': 'Jerry'},
                                    {'age': 35, 'name': 'Jerry'}]
        """
        tmp_list = copy.copy(src_list)
        ret_list = []
        while True:
            index = FuncLib.index(predicate, tmp_list)
            if index == -1:
                break
            else:
                ret_list.append(tmp_list[index])
                if index < len(tmp_list) - 1:
                    tmp_list = tmp_list[index + 1:]
                else:
                    break
        return ret_list

    @staticmethod
    def reject(predicate, src_list):
        """
        ### fn.reject
            Returns the values in list without the elements that the truth test (predicate)
            passes.
            The opposite of filter.
            eg:
                persons = [{"name": "Tom", "age": 12},
                            {"name": "Jerry", "age": 20},
                            {"name": "Mary", "age": 35}]
                not_Mary = fn.reject({"name": "Mary"}, persons)
                adults = fn.reject(lambda x: x['age'] < 18, persons)
                print(not_Mary)  # => [{"age": 12, "name": "Tom"},
                                        {"age": 20, "name": "Jerry"}]
                print(adults)    # => [{"age": 20, "name": "Jerry"},
                                        {"age": 35, "name": "Mary"}]
        """
        index = FuncLib.index(predicate, src_list)
        if index != -1:
            tmp_list = copy.copy(src_list)
            del tmp_list[index]
            return FuncLib.reject(predicate, tmp_list)
        return src_list

    @staticmethod
    def reduce(*args):
        """
        ### fn.reduce
            Returns the buildIn method 'reduce', in python 3 the 'reduce' is imported
            from functools.
            eg:
                num_list = [1 , 2, 3, 4]
                fn.reduce(lambda a, b: a + b, num_list)  # => 10
        """
        return reduce(*args)

    @staticmethod
    def contains(predicate, src_list):
        """
        ### fn.contains
            Returns true if the value is present in the list.
            eg:
                persons = [{"name": "Tom", "age": 12},
                            {"name": "Jerry", "age": 20},
                            {"name": "Mary", "age": 35}]
                fn.contains({"name": "Jerry", "age": 12}, persons)  # => False
                fn.contains(lambda x: x['name'] == 'Mary', persons) # => True
        """
        index = FuncLib.index(predicate, src_list)
        return index != -1

    @staticmethod
    def flatten(src_list, is_deep=False):
        """
        ### fn.flatten
            Flattens a nested array (the nesting can be to any depth). If you pass shallow,
            the array will only be flattened a single level.
            eg:
                fn.flatten([1, [2], [3, [[4]]]])        # => [1, 2, 3, [[4]]]
                fn.flatten([1, [2], [3, [[4]]]], True)  # => [1, 2, 3, 4] 
        """
        if src_list and FuncLib.typeof(src_list, 'lst', 'map', 'tup'):
            tmp_list = []
            for item in src_list:
                if isinstance(item, list):
                    if is_deep:
                        tmp_list += FuncLib.flatten(item, True)
                    else:
                        tmp_list += item
                else:
                    tmp_list.append(item)
            return tmp_list
        return src_list

    @staticmethod
    def uniq(src_list, path='/'):
        """
        ### fn.uniq
            Produces a duplicate-free version of the array.
            In particular only the first occurence of each value is kept.
            eg:
                persons00 = ("Tom", "Tom", "Jerry")
                persons01 = ["Tom", "Tom", "Jerry"]
                demo_list = [False, [], False, True, [], {}, False, '']
                persons02 = [{"name": "Tom", "age": 12, "pet": {"species": "dog", "name": "Kitty"}},
                                {"name": "Tom", "age": 20, "pet": {"species": "cat", "name": "wang"}},
                                {"name": "Mary", "age": 35, "pet": {"species": "cat", "name": "mimi"}}]
                fn.uniq(persons00)  # => ["Jerry", "Tom"]
                fn.uniq(persons01)  # => ["Jerry", "Tom"]
                fn.uniq(demo_list)  # => [False, [], True, {}, '']
                fn.uniq(persons02, '/name')
                fn.uniq(persons02, '/pet/species')
        """
        tmp_list = FuncLib.__listlize(copy.copy(src_list))
        if tmp_list and FuncLib.typeof(tmp_list, list):
            paths = FuncLib.drop(path.split('/'));
            if len(paths) == 0:
                for i in range(0, len(tmp_list)):
                    if len(tmp_list) <= i + 1:
                        break
                    tmp_list = tmp_list[:i + 1] + FuncLib.reject(
						lambda x: x == tmp_list[i], tmp_list[i + 1:])
            else:
                for i in range(0, len(tmp_list)):
                    if len(tmp_list) <= i + 1:
                        break
                    tmp_list = tmp_list[:i + 1] + FuncLib.reject(
                        lambda x: FuncLib.__cpr_val(paths, x, tmp_list[i]), tmp_list[i + 1:])
        return tmp_list
    
    @staticmethod
    def __cpr_val(paths, dict1, dict2):
        v1 = FuncLib.__get_val(paths, dict1)
        v2 = FuncLib.__get_val(paths, dict2)
        return  v1[0] and v2[0] and v1[1] == v2[1]
    
    @staticmethod
    def __get_val(paths, _dict):
        tmp_val = _dict
        for i in range(0, len(paths)):
            if FuncLib.typeof(tmp_val, dict) and paths[i] in tmp_val:
                tmp_val = tmp_val[paths[i]]
            else:
                return False, None
        return True, tmp_val

    @staticmethod
    def pluck(body, *keys, **conf):
        """
        ### fn.pluck
            Pluck the collections element.
            eg:
                persons = [{"name": "Tom", "hobbies": ["sing", "running"]},
                    {"name": "Jerry", "hobbies": []},
                    {"name": "Mary", "hobbies": ['hiking', 'sing']}]
                hobbies = fn.pluck(persons, 'hobbies')
                uniq_hobbies = fn.pluck(persons, 'hobbies', uniq=True)
                print(hobbies)      # => ["sing", "running", 'hiking', 'sing']
                print(hobbies_uniq) # => ["sing", "running", 'hiking']
        """
        if isinstance(body, dict):
            tmp_body = [body]
        else:
            tmp_body = body
        if FuncLib.typeof(tmp_body, 'lst', 'map', 'tup'):
            for key in keys:
                field_k = list(map(lambda x: x[key], tmp_body))
                if len(field_k) > 0:
                    tmp_body = reduce(FuncLib.tolist, field_k)
                tmp_body = FuncLib.tolist(tmp_body)
            if FuncLib.get(conf, '/is_uniq', 'bol'):
                tmp_body = FuncLib.uniq(tmp_body)
        return tmp_body

    @staticmethod
    def every(predicate, src_list):
        """
        ### fn.every
            Returns true if all of the values in the list pass the predicate truth test.
            Short-circuits and stops traversing the list if a false element is found.
            eg:
                num_list = [1, 1, 2, 3, 5, 8]
                persons = [{"name": "Tom", "age": 12, "sex": "m"},
                            {"name": "Jerry", "age": 20, "sex": "m"},
                            {"name": "Mary", "age": 35, "sex": "f"}]
                fn.every(5, num_list)                       # => False
                fn.every({"sex": "m"}, persons)             # => False
                fn.every(lambda x: x['age'] > 18, persons)  # => False
        """
        if src_list and FuncLib.typeof(src_list, list, map, tuple):
            for item in src_list:
                if predicate != item:
                    if isinstance(predicate, dict):
                        for key in predicate:
                            if key not in item or predicate[key] != item[key]:
                                return False
                    elif FuncLib.typeof(predicate, 'fun'):
                        if not bool(predicate(item)):
                            return False
                    else:
                        return False
            return True
        return False

    @staticmethod
    def some(predicate, src_list):
        """
        ### fn.some
            Returns true if any of the values in the list pass the predicate
            truth test. Short-circuits and stops traversing the list if a true
            element is found.
            eg:
                num_list = [1, 1, 2, 3, 5, 8]
                persons = [{"name": "Tom", "age": 12, "sex": "m"},
                            {"name": "Jerry", "age": 20, "sex": "m"},
                            {"name": "Mary", "age": 35, "sex": "f"}]
                fn.some(5, num_list)                       # => True
                fn.some({"sex": "m"}, persons)             # => True
                fn.some(lambda x: x['age'] > 18, persons)  # => True
        """
        if src_list and FuncLib.typeof(src_list, list, map, tuple):
            for item in src_list:
                if predicate != item:
                    if isinstance(predicate, dict):
                        tmp_bool = True
                        for key in predicate:
                            if key not in item or predicate[key] != item[key]:
                                tmp_bool = False
                        if tmp_bool:
                            return True
                    elif FuncLib.typeof(predicate, 'fun'):
                        if bool(predicate(item)):
                            return True
                else:
                    return True
            return False
        return False

    @staticmethod
    def tolist(*values):
        """
        ### fn.tolist
            Return a listlized value.
            eg:
                fn.tolist()       # => []
                fn.tolist([])     # => []
                fn.tolist({})     # => [{}]
                fn.tolist(None)   # => [None]
                fn.tolist('str')  # => ['str']
        """
        def list_handler(val):
            if isinstance(val, list):
                return val
            return [val]

        if len(values) == 0:
            return []
        elif len(values) == 1:
            return list_handler(values[0])
        else:
            return reduce(lambda a, b: list_handler(a) + list_handler(b), values)

    @staticmethod
    def drop(src_list, is_without_0=False):
        """
        ### fn.drop
            Delete false values expect 0.
            eg:
                tmp_list = [0, '', 3, None, [], {}, ['Yes'], 'Test']
                fn.drop(tmp_list)        # => [3, ['Yes'], 'Test']
                fn.drop(tmp_list, True)  # => [0, 3, ['Yes'], 'Test']
        """
        if bool(src_list):
            if FuncLib.typeof(src_list, tuple, map):
                src_list = list(src_list)
            if isinstance(src_list, list):
                tmp_list = []
                for item in src_list:
                    if bool(item) or (is_without_0 and item == 0):
                        tmp_list.append(item)
                return tmp_list
        return src_list

    @staticmethod
    def typeof(value, *types):
        """
        ### fn.typeof
            Verify is value in given types. types should be one or some
            key or value in the types_map below.
            types_map: {
                'int': int,
                'flt': float,
                'str': str,
                'bol': bool,
                'dic': dict,
                'lst': list,
                'tup': tuple,
                'uni': 'unicode',   
                'non': 'NoneType',
                'fun': 'function',
                'kis': 'dict_keys',
            }
            eg: 
                fn.typeof(None, 'non')                # => True
                fn.typeof(True, 'str')                # => False
                fn.typeof([], 'map', 'lst', 'tup')    # => True
                fn.typeof(lambda x: x, 'fun')         # => True
        """
        types_map = {
            'int': int,
            'flt': float,
            'str': str,
            'bol': bool,
            'dic': dict,
            'lst': list,
            'tup': tuple,
            'uni': 'unicode',   
            'non': 'NoneType',
            'fun': 'function',
        }
        if len(types) > 0:
            def is_type_of(tp):
                if isinstance(tp, type):
                    return isinstance(value, tp)
                else:
                    return str(tp) in str(type(value))

            for _type in types:
                if is_type_of(_type) or (_type in types_map and is_type_of(types_map[_type])):
                    return True
        return False
    
    @staticmethod
    def typeval(value, *types):
        """
        ### fn.clear
            Verify is value in given types. retury The value self or False by typeof check.
            eg: 
                fn.typeval('test', 'str')  # => 'test'
                fn.typeval([], 'lst')  # => []
                fn.typeval({}, 'lst')  # => False
        """
        if len(types) > 0:
            if not FuncLib.typeof(value, *types):
                return False
        return value

    @staticmethod
    def get(origin, path, *types):
        """
        ### fn.get
            Get values form dict or list.
            eg:
                Tom = {
                    "name": "Tom",
                    "age": 12,
                    "pets": [
                        {"species": "dog", "name": "Kitty"},
                        {"species": "cat", "name": "mimi"}
                    ]
                }
                fn.get(Tom, '/age')             # => 12
                fn.get(Tom, '/pets/0/species')  # => dog
                fn.get(Tom, '/pets/1/name')     # => mimi
        """
        if origin and path:
            tmp_val = origin
            paths = FuncLib.drop(path.split('/'));
            for pt in paths:
                if pt in tmp_val:
                    tmp_val = tmp_val[pt]
                else:
                    tmp_val = FuncLib.__listlize(tmp_val)
                    if FuncLib.typeof(tmp_val, 'lst')\
                        and FuncLib.iscan('int(%s)' %pt) and len(tmp_val) >= int(pt):
                        tmp_val = tmp_val[int(pt)]
                    else:
                        return None
            return FuncLib.typeval(tmp_val, *types)
        return None

    @staticmethod
    def dump(_json, **conf):
        """
        ### fn.dump
            Return a formatted json string.
            eg:
                persons = [{"name": "Tom", "hobbies": ["sing", "running"]},
                    {"name": "Jerry", "hobbies": []}]
                print(fn.dump(persons)) #=>
                [
                    {
                    "hobbies": [
                        "sing", 
                        "running"
                    ], 
                    "name": "Tom"
                    }, 
                    {
                    "hobbies": [], 
                    "name": "Jerry"
                    }
                ]
        """
        FuncLib.__listlize(_json)
        if FuncLib.typeof(_json, 'lst', 'dic'):
            is_sort = FuncLib.get(conf, '/sort_keys') or True
            idt = FuncLib.get(conf, '/indent') or True
            return json.dumps(_json, sort_keys=True, indent=2)
        return _json

    @staticmethod
    def test(pattern, origin):
        """
        ### fn.test
            Varify is the match successful, a boolean value will be returned.
            eg:
                fn.test(r'ab', 'Hello World!')  # => False
                fn.test(r'll', 'Hello World!')  # => True
        """
        return re.search(pattern, origin) is not None

    @staticmethod
    def replace(*args):
        """
        ### fn.replace
            Replace sub string of the origin string with re.sub()
            eg:
                greetings = 'Hello I\'m Tom!'
                print(fn.replace(r'Tom', 'Jack', greetings)) # => Hello I'm Jack!
        """
        return re.sub(*args)

    @staticmethod
    def iscan(exp):
        """
        ### fn.iscan
            Test is the expression valid, a boolean value will be returned.
            eg:
                print(fn.iscan("int('a')"))  # => False
                print(fn.iscan("int('5')"))  # => True
        """
        if isinstance(exp, str):
            try:
                exec (exp)
                return True
            except:
                return False
        return False

    @staticmethod
    def log(*values, **conf):
        """
        ### fn.log
            Show log clear in console.
            eg:
                persons = [{"name": "Tom", "hobbies": ["sing", "running"]}]
                fn.log(persons)  # =>
        ==========================================================
                            [12:22:35] funclib 2.1.5
        ----------------------------------------------------------
        [
            {
                "hobbies": [
                    "sing", 
                    "running"
                ], 
                "name": "Tom"
            }
        ]
        ==========================================================
        """
        width = 68
        if 'width' in conf and FuncLib.typeof(conf['width'], 'int') and conf['width'] > 40:
            width = conf['width']
        line_b = '=' * width
        line_m = '-' * width
        line_s = '- ' * int((width / 2))
        if 'end' in conf and FuncLib.typeval(conf['end'], 'bol'):
            print('%s\n' % line_b)
            return
        time_info = "[" + time.strftime("%H:%M:%S", time.localtime()) + "] "
        title = time_info + log_title
        if 'title' in conf and str(conf['title']):
            tt = time_info + str(conf['title'])
            title = len(tt) <= 35 and tt or tt[:35]
        title = ' ' * int((width - len(title)) / 2) + title
        print('\n%s\n%s\n%s' % (line_b, title, line_m))
        if 'pre' in conf and FuncLib.typeval(conf['pre'], 'bol'):
            return
        if len(values) > 0:
            for i in range(0, len(values)):
                if i > 0:
                    print(line_s)
                print(FuncLib.dump(values[i]))
        else:
            print('None')
        print('%s\n' % line_b)

    @staticmethod
    def timer(func, times=60, interval=1):
        """
        ### fn.timer
            Set a timer with interval and timeout limit.
            eg: 
                count = 0
                def fn():
                    global count
                    if count == 4:
                        return True
                    count += 1
                    print(count)
                fn.timer(fn, 10, 2)
                # =>
                    >>> 1  #at 0s
                    >>> 2  #at 2s
                    >>> 3  #at 4s
                    >>> 4  #at 4s
        """
        if not FuncLib.typeof(func, 'fun')\
            or not isinstance(times, int)\
            or not isinstance(interval, int)\
            or times < 1 or interval < 0:
            return
        is_time_out = False
        count = 0
        while True:
            count += 1
            if count == times:
                func()
                is_time_out = True
                break
            elif func():
                break
            time.sleep(interval)
        return is_time_out

    @staticmethod
    def now():
        """
        ### fn.now
            Return system now time.
            eg: 
                fn.now()    #=> 2018-07-26 14:34:26
        """
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    @staticmethod
    def clear():
        """
        ### fn.clear
            Clear the terminam screen.
            eg: 
                >>> from funclib import fn
                >>> fn.clear()
        """
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def __listlize(list_like):
        if FuncLib.typeof(list_like, 'map', 'tup', 'kis'):
            return list(list_like)
        return list_like
