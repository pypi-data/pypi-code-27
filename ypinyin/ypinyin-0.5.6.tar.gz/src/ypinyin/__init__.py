import os
import xpinyin

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), \
                                                'Mandarin.dat')
sc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), \
                                                        'special_characters.dat')
class Pinyin(xpinyin.Pinyin):

    """translate chinese hanzi to pinyin by python, inspired by flyerhzm’s
    `chinese\_pinyin`_ gem

    usage
    -----
    ::

        >>> from ypinyin import Pinyin
        >>> p = Pinyin()
        >>> # default splitter is `-`
        >>> p.get_pinyin(u"上海")
        'shang-hai'
        >>> # show tone marks
        >>> p.get_pinyin(u"上海", show_tone_marks=True)
        'shàng-hǎi'
        >>> # remove splitter
        >>> p.get_pinyin(u"上海", '')
        'shanghai'
        >>> # set splitter as whitespace
        >>> p.get_pinyin(u"上海", ' ')
        'shang hai'
        >>> p.get_initial(u"上")
        'S'
        >>> p.get_initials(u"上海")
        'S-H'
        >>> p.get_initials(u"上海", u'')
        'SH'
        >>> p.get_initials(u"上海", u' ')
        'S H'

    请输入utf8编码汉字
    .. _chinese\_pinyin: https://github.com/flyerhzm/chinese_pinyin
    """

    def __init__(self, data_path = data_path, sc_path=sc_path):
        xpinyin.Pinyin.__init__(self, data_path=data_path) 
       	self.sc_dict = {}
        with open(sc_path) as f:
            for line in f:
                k, v = line.split()
                self.sc_dict[k] = v.strip()                                        

    def get_pinyin(self, chars=u'你好', splitter=u'-',
                   show_tone_marks=False, convert='lower'):
        for e in self.sc_dict:
            if e in chars:
                chars = chars.replace(e, self.sc_dict[e])
        return super(Pinyin,self).get_pinyin(chars, splitter, \
                                        show_tone_marks, convert)
