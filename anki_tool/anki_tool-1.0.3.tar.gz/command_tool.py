import os
import random
import re
import time
from sys import argv

from anki.data_query import DataQuery
from configuration import Configuration
from anki import __version__


def main():
    warning = "-w                            - default input word mode,word from command.\n" \
              "-f                            - word from disk file.\n" \
              "-v                            - application version.\n" \
              "--import                      - import all resource files.\n" \
              "--config                      - dict path,or generate file path..."
    if 1 == len(argv):
        print(warning)
    else:
        command = argv[1]
        if command == "-w":
            import_data(argv[2:])
        elif command == "-f":
            import_file(argv[2:])
        elif command == "-v":
            print("current version is %s" % __version__)
        elif command == "--import":
            import_resources()
        elif command == "--config":
            open_config()
        else:
            # 检测是否为单词，如果是的话，以单词处理
            if not import_args(argv[1:]):
                print(warning)


def import_args(param):
    """导入参数"""
    result = True
    pattern = re.compile(r"([\w\-\s]+)")
    for arg in param:
        result &= (re.fullmatch(pattern, arg) is not None)
    if result:
        # 一行8个，以20个字符为一个单元信息
        print("检测到你输入了:%d 个单词" % len(param))
        for index in range(0, len(param)):
            print(param[index].ljust(20, ' '), end='')
            if 0 != index and 0 == index % 8: print()
        print()
        print("是否导入！(y/n)")
        input_str = input("> ")
        if "yes" == input_str.lower() or 'y' == input_str.lower():
            #  导入单词
            import_data(param)
    return result


def import_resources():
    """导入资源文件"""
    data_query = DataQuery()
    data_query.import_resources(Configuration())


def open_config():
    # 打开配置文件
    config = Configuration()
    os.system("explorer.exe /n, %s" % config.app_config_file.replace("/", os.path.sep))


def import_file(param):
    items = []
    if 0 == len(param):
        print("please select a word txt file!")
    else:
        for path in param:
            if os.path.exists(path):
                try:
                    file = open(path, "r")
                    items.extend(list(map(lambda i: i.strip(), file.readlines())))
                    file.close()
                except Exception as e:
                    print("\t文件:%s读取异常！" % path)
                    print(e)
        print("共%d个文件，共检测到:%d 个单词" % (len(param), len(items)))
        for index in range(0, len(items)):
            print(items[index].ljust(20, ' '), end='')
            if 0 != index and 0 == index % 8: print()
        print()
        print("\t是否导入！(y/n)")
        input_str = input("> ")
        if "yes" == input_str.lower().strip() or 'y' == input_str.lower().strip():
            #  导入单词
            import_data(items)
        else:
            print("import task abort!")


def import_data(data):
    """导入数据"""
    data_query = DataQuery()
    data_query.process(Configuration(), data)
