"""这是nester.py模块，提供了一个名为print_lol函数，该函数的作用是打印列表，其中可能包含或不包含嵌套列表。"""
def print_lol(the_list, indent=false, level=0， fn=sys.stdout):
    """这个函数取一个位置参数，名为”the_list“,这可以是任何Python列表（也可以是包含嵌套列表的列表）。所指定的
    列表中的每个数据项会（递归地）输出到屏幕上，各数据项各占一行"""
    """第二个参数（level）用来在遇到嵌套列表时插入制表符,增加一个缺省值（赋初值），使其变为可选参数"""
    """第三个参数（indent）用来实现控制缩进特性，增加一个缺省值（false），默认关闭缩进"""
    """第四个参数（fn）用来实现把数据输出到一个磁盘文件，增加一个缺省值（sys.stdout),默认输出至屏幕"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fn)
        else:
            if indent:  #增加一行代码控制何时缩进
                for tap in range(level):
                    print("\t", end='', file=fn)
            print(each_item, file=fn)
