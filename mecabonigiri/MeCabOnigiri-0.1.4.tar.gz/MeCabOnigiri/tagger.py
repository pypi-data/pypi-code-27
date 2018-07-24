import MeCab


def get_mecab_tagger(option='-Owakati'):
    m = MeCab.Tagger(option)
    # https://qiita.com/kasajei/items/0805b433f363f1dba785
    m.parse("")
    return m
