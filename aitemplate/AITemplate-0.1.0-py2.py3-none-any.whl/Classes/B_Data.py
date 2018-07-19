# -*- coding: utf-8 -*-
# @Time    : 2018/7/19 下午5:17
# @Author  : ZZZ
# @Email   : zuxinxing531@pingan.com.cn
# @File    : bData.py
# @Software: Template
# @Descript: bData

from interface import Interface

class B_Data(Interface):
    def __init__(self):
        '''数据类初始化
        '''
        pass

    def set_file_path(self,fp,*args):
        '''设置数据读取目录
        Args:
            fp:文件目录
        '''
        pass

    def read_data_from_file(self,format="default",*args):
        '''读取数据
        Args:
            format:读取后返回的数据格式(由开发者自定义)
        '''
        pass

    def get_data(self,*args):
        '''获取数据并返回
        Returns:
            data:从文件读取到的数据
        '''
        pass

    def save_data_to_path(self,path,rewrite=False,*args):
        '''保存数据
        Args:
            path:保存目录
            rewrite:是否覆盖,默认False
        '''
        pass

if __name__ == "__main__":
    pass