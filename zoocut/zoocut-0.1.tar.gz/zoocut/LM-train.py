from math import log
import pickle
import sys

if __name__ == '__main__':
    print("训练LM")

    if len(sys.argv) == 1:
        arg = '_chinese_corpus'
    else:
        arg = '_weibo'

    data = []
    with open('./data/train%s.txt' % arg, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(line.replace('\n', '').replace(' ', ''))

    print("语料:%d" % len(data))

    dict = set()
    for i in data:
        for j in i.split(' '):
            dict.add(i)
    with open('data/dict%s.txt' % arg, 'a', encoding='utf-8') as f:
        for i in dict:
            r = f.write("%s\n" % i)
    print("词典：%d" % len(dict))

    # `表示开始，~表示结束
    for i in range(len(data)):
        data[i] = '` ' + data[i] + ' ~'

    # 词典
    words = set()
    for i in data:
        for j in i.split(' '):
            if j not in words:
                words.add(j)

    times = {}  # 单词出现的次数
    for i in data:
        for j in i.split(' '):
            if j not in times:
                times[j] = 1
            else:
                times[j] += 1
    count = {}  # 双词前后共现次数
    for i in range(len(data)):
        ss = data[i].split(' ')
        for j in range(len(ss) - 1):
            if (ss[j], ss[j + 1]) not in count:
                count[(ss[j], ss[j + 1])] = 1
            else:
                count[(ss[j], ss[j + 1])] += 1

    # 加1法平滑
    granm = {}  # 2-granm语言模型
    zeros = {}  # 2-granm中不存在的词对
    for (i, j) in count:
        granm[(i, j)] = (1 + count[(i, j)]) / (len(words) + times[i])
    for i in times:
        zeros[i] = 1 / (len(words) + times[i])

    f = open("./lm/model.pkl", 'wb')
    pickle.dump((granm, zeros), f)
    f.close()
    print("LM训练完成")