#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    Author:cleverdeng
    E-mail:clverdeng@gmail.com
"""

__version__ = '0.9'
__all__ = ["PinYin"]

import os.path

word_data='''

'''


class PinYin(object):
    def __init__(self, dict_file='word.data'):
        self.word_dict = {}
        self.dict_file =dict_file
        print(self.dict_file)


    def load_word(self):
        if not os.path.exists(self.dict_file):
            raise IOError("NotFoundFile")

        with file(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                try:
                    line = f_line.split('    ')
                    self.word_dict[line[0]] = line[1]
                except:
                    line = f_line.split('   ')
                    self.word_dict[line[0]] = line[1]



    def hanzi2pinyin_array(self, string=""):
        result = []
        if not isinstance(string, unicode):
            string = string.decode("utf-8")
        
        for char in string:
            key = '%X' % ord(char)
            result.append(self.word_dict.get(key, char).split()[0][:-1].lower())

        return result


    def hanzi2pinyin_split(self, string="", split=""):
        result = self.hanzi2pinyin_array(string=string)
        if split == "":
            return result
        else:
            return split.join(result)

    def hanzi2pinyin(self,string=""):
        result=self.hanzi2pinyin_array(string)
        result = ''.join(result)
        return result


if __name__ == "__main__":
    print(os.path.dirname(__file__))
    print(os.path.dirname(os.path.dirname(__file__)))
    test = PinYin()
    test.load_word()
    string = u"崂山"
    print "in: %s" % string
    print "out: %s" % str(test.hanzi2pinyin(string=string))
    print "out: %s" % test.hanzi2pinyin_split(string=string, split="-")

