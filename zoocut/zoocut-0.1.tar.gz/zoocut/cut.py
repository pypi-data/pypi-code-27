import pickle
import math
from queue import Queue
from functools import wraps
import time
import sys

# 测量函数运行时间
def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        print("start run %s " % (function.__name__))
        sys.stdout.flush()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("end run %s: %s seconds" % (function.__name__, str(t1-t0)))
        return result
    return function_timer

# 生成全切分用的词树用的节点
class Node:
    def __init__(self, data, id, parent=None, p=1):
        self.data = data
        self.id = id
        self.child_list = []  # 子节点列表
        self.parent = parent  # 父亲节点
        self.p = p  # 当前概率

    def add_child(self, leaf):
        self.child_list.append(leaf)

# 分词器
class Cut(object):
    def __init__(self, arg='_chinese_corpus'):
        # 初始化基于词典的方法
        self.dict = set([i.split(' ')[0].replace('\n', '') for i in open("./data/dict%s.txt" % arg, 'r', encoding='utf-8')])
        if '' in self.dict:
            self.dict.remove('')
        self.max_length = max([len(i) for i in self.dict])
        # 初始化基于马尔可夫模型的方法
        self.prob_start = pickle.load(open('./hmm/prob_start%s.pkl' % arg, 'rb'))  # 初始状态概率
        self.prob_trans = pickle.load(open('./hmm/prob_trans%s.pkl' % arg, 'rb'))  # 转移概率
        self.prob_emit = pickle.load(open('./hmm/prob_emit%s.pkl' % arg, 'rb'))  # 发射概率
        # 初始化基于语言模型的方法
        self.language_model = pickle.load(open('./lm/model%s.pkl' % arg, 'rb'))  # 2-granm语言模型

    # 后向最大匹配
    def BMM(self, s):
        max_length = self.max_length
        s_end = len(s)
        w_split = []
        while True:
            s_length = s_end - 0
            if s_length == 0:
                return [w_split[len(w_split) - i - 1] for i in range(len(w_split))]
            elif s_length < max_length:
                max_length = s_length
            w2 = s[s_end - max_length:s_end]
            shift = 1
            while len(w2) > 0:
                if w2 in self.dict:
                    w_split.append(w2)  # 加入分好词的list中
                    break
                elif len(w2) > 1:
                    w2 = s[s_end - max_length + shift:s_end]
                    shift += 1
                else:
                    # w1是单字，并且词典中无该字
                    w_split.append(w2)
                    self.dict.add(w2)
                    break
            s_end -= len(w2)

    # 前向最大匹配
    def FMM(self, s):
        max_length = self.max_length
        s_start = 0
        w_split = []
        while True:
            s_length = len(s) - s_start
            if s_length == 0:
                return w_split
            elif s_length < max_length:
                max_length = s_length
            w1 = s[s_start:s_start + max_length]
            shift = 1
            while len(w1) > 0:
                if w1 in self.dict:
                    w_split.append(w1)  # 加入分好词的list中
                    break
                elif len(w1) > 1:
                    w1 = s[s_start:s_start + max_length - shift]
                else:
                    # w1是单字，并且词典中无该字
                    w_split.append(w1)
                    self.dict.add(w1)
                shift += 1
            s_start += len(w1)

    # 双向最大匹配
    def BiMM(self, s):
        f_result = self.FMM(s)
        b_result = self.BMM(s)
        if len(f_result) == len(b_result):  # 正反向分词结果词数相同
            if set(f_result) == set(b_result):  # 两个分词结果一样，随便选一个
                return b_result
            else:  # 结果不同，返回单字较少的那个
                f_result_sorted = sorted(f_result, key=lambda f: len(f))
                b_result_sorted = sorted(b_result, key=lambda b: len(b))
                f_min_length, b_min_length = len(f_result_sorted[0]), len(b_result_sorted[0])
                if f_min_length == b_min_length:  # 返回最短词最少的结果
                    f_min_count, b_min_count = 0, 0
                    for i in f_result_sorted:
                        if len(i) == f_min_length:
                            f_min_count += 1
                    for i in b_result_sorted:
                        if len(i) == b_min_length:
                            b_min_count += 1
                    # 若最短词长度相同，默认bmm
                    result = f_result if f_min_count < b_min_count else b_result
                else:
                    result = f_result if f_min_length > b_min_length else b_result
                return result
        else:  # 正反向分词结果词数不同，取分词数量较少的那一个
            result = f_result if len(b_result) > len(f_result) else b_result
            return result

    # 基于隐马尔科夫模型的方法
    def HMM(self, s):
        def prob_log(prob):
            if prob == 0:
                return -float('inf')
            else:
                return math.log2(prob)

        states = ['B', 'M', 'E', 'S']  # 状态值集合
        V = [{}]
        path = {}
        for y in states:  # 初始值
            V[0][y] = prob_log(self.prob_start[y]) + prob_log(self.prob_emit[y].get(s[0], 0))  # 在位置0，以y状态为末尾的状态序列的最大概率
            path[y] = [y]
        for t in range(1, len(s)):
            V.append({})
            newpath = {}
            for y in states:  # 从y0 -> y状态
                (prob, state) = max([(V[t - 1][y0] + prob_log(self.prob_trans[y0].get(y, 0)) + prob_log(self.prob_emit[y].get(s[t], 0)), y0) for y0 in states])
                V[t][y] = prob
                newpath[y] = path[state] + [y]
            path = newpath  # 记录状态序列
        l = []
        for y in states:
            l.append((V[len(s) - 1][y], y))
        (prob, state) = max(l)
        result_path = path[state]
        word_list = []
        word = ''
        for i in range(len(s)):
            if result_path[i] == 'B' or result_path[i] == 'M':
                word += s[i]
            elif result_path[i] == 'E':
                word += s[i]
                word_list.append(word)
                word = ''
            elif result_path[i] == 'S':
                word_list.append(s[i])
        return word_list

    # 基于语言模型的方法
    def LM(self, s):
        lists = []  # 词列表
        for i in range(len(s)):
            list_t = []
            for j in range(i + 1, len(s) + 1):
                if s[i:j] in set(self.dict):
                    list_t.append(s[i:j])
            if len(list_t) == 0:
                list_t.append(s[i: i+1])
            lists.append(list_t)
        # 创建词树中的一个节点
        root = Node('<BOS>', 0, None, 1)
        stack = []
        max_p = 0
        best = None
        for word in lists[0]:  # 根节点的子节点
            if ('<BOS>', word) in self.language_model[0]:  # 2-granm中有
                p = self.language_model[0][('<BOS>', word)]
            elif '<BOS>' in self.language_model[1]:  # 2-granm中没有，加一平滑
                p = self.language_model[1]['<BOS>']
            else:
                p = 1
            child = Node(word, 1, root, p)
            root.add_child(child)
            stack.append(child)
        while len(stack) > 0:
            node = stack.pop()
            new_id = node.id + len(node.data)
            if new_id <= len(lists):  # 不是叶子节点
                for word in lists[new_id - 1]:
                    if (node.data, word) in self.language_model[0]:  # 2-granm中有
                        p = node.p * self.language_model[0][(node.data, word)]
                    elif node.data in self.language_model[1]:  # 2-granm中没有，加一平滑
                        p = node.p * self.language_model[1][node.data]
                    else:
                        p = node.p * 1
                    if p < max_p:
                        continue
                    child = Node(word, new_id, node, p)
                    node.add_child(child)
                    stack.append(child)
            else:  # 加入叶子节点
                child = Node('<EOS>', new_id, node, node.p)
                node.add_child(child)
                if node.p > max_p:
                    max_p = p
                    best = child
        result = []
        while True:
            result.append(best.data)
            best = best.parent
            if best is None:
                break
        result = result[1: -1]
        result.reverse()
        return result

    # 调用分词
    def cut(self, sentence, function=BMM):
        return function(sentence)
