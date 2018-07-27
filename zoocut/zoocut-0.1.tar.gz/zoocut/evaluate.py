from cut import *
from functools import wraps
import time
import sys

# 测量函数运行时间
def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        print("Total time running %s: " % (function.__name__), end=' ')
        sys.stdout.flush()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("%s seconds" % str(t1-t0))
        return result
    return function_timer

@fn_timer
def test(data, self, model):
    p_t = []
    r_t = []
    for test in data:
        result = ' '.join(self.cut(test.replace(' ', ''), model))
        old = set(test.split(' '))
        new = set(result.split(' '))
        p = len(old & new) / len(new)
        r = len(old & new) / len(old)
        p_t.append(p)
        r_t.append(r)
    p = sum(p_t) / len(p_t)
    r = sum(r_t) / len(r_t)
    f = 2 * p * r / (p + r)
    return f, p, r


if __name__ == '__main__':
    if len(sys.argv) == 1:
        arg = '_chinese_corpus'
    else:
        arg = '_weibo'

    self = Cut(arg=arg)
    data = []
    with open('./data/test%s.txt' % arg, 'r', encoding='utf-8') as f:
        for line in f:
            if line != '\n':
                data.append(line.replace(' \n', ''))

    f, p, r = test(data, self, self.BMM)
    print("BMM: f值：%f 准确率：%f 召回率：%f" % (f, p, r))
    f, p, r = test(data, self, self.FMM)
    print("FMM: f值：%f 准确率：%f 召回率：%f" % (f, p, r))
    f, p, r = test(data, self, self.BiMM)
    print("BiMM: f值：%f 准确率：%f 召回率：%f" % (f, p, r))
    f, p, r = test(data, self, self.HMM)
    print("HMM: f值：%f 准确率：%f 召回率：%f" % (f, p, r))
    f, p, r = test(data, self, self.LM)
    print("LM: f值：%f 准确率：%f 召回率：%f" % (f, p, r))

