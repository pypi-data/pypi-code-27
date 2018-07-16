import MeCab


def get_mecab_tagger(option='-Owakati'):
    m = MeCab.Tagger(option)
    return m
