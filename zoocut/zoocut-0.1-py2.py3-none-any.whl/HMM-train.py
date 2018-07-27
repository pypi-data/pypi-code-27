"""一阶HMM"""
import pickle
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        arg = '_chinese_corpus'
    else:
        arg = '_weibo'

    A_dic = {}  # 转移概率矩阵alpha
    B_dic = {}  # 发射概率矩阵beta
    Pi_dic = {}  # 初始状态概率
    word_set = set()  # 观察值集合（即语料库中出现的字，set去重）
    state_list = ['B', 'M', 'E', 'S']  # 状态值集合
    Count_dic = {}
    line_num = -1  # 初始是-1

    INPUT_DATA = "./data/train%s.txt" % arg  # 训练数据
    PROB_START = "./hmm/prob_start%s.pkl" % arg # 初始状态概率
    PROB_TRANS = "./hmm/prob_trans%s.pkl" % arg # 转移概率
    PROB_EMIT = "./hmm/prob_emit%s.pkl" % arg # 发射概率


    def init():  # 初始化字典
        for state in state_list:
            A_dic[state] = {}
            for state1 in state_list:
                A_dic[state][state1] = 0.0
        for state in state_list:
            Pi_dic[state] = 0.0
            B_dic[state] = {}
            Count_dic[state] = 0


    def getList(input_str):  # 输入观察序列，输出内部状态
        output_str = []
        if len(input_str) == 1:
            output_str.append('S')
        elif len(input_str) == 2:
            output_str = ['B', 'E']
        else:
            output_str.append('B')
            output_str.extend('M' * (len(input_str) - 2))
            output_str.append('E')
        return output_str


    def Output():  # 输出模型的三个参数：初始概率+转移概率+发射概率
        start_output = open(PROB_START, 'wb')
        emit_output = open(PROB_EMIT, 'wb')
        trans_output = open(PROB_TRANS, 'wb')

        for key in Pi_dic:  # 状态的初始概率
            Pi_dic[key] = Pi_dic[key] * 1.0 / line_num
        pickle.dump(Pi_dic, start_output)

        for key in A_dic:  # 状态转移概率
            for key1 in A_dic[key]:
                A_dic[key][key1] = A_dic[key][key1] / Count_dic[key]
        pickle.dump(A_dic, trans_output)

        for key in B_dic:  # 发射概率(状态->词语的条件概率)
            for word in B_dic[key]:
                B_dic[key][word] = B_dic[key][word] / Count_dic[key]
        pickle.dump(B_dic, emit_output)

        start_output.close()
        emit_output.close()
        trans_output.close()


    if __name__ == "__main__":
        input_file = open(INPUT_DATA, encoding='utf-8')
        init()
        for line in input_file:
            if line == '\n':
                continue
            line_num += 1
            if line_num % 10000 == 0:
                print(line_num)
            line = line.strip()
            word_list = []
            for i in range(len(line)):
                if line[i] != ' ':
                    word_list.append(line[i])  # 存放该行的每个单字，即观察序列
                    word_set.add(line[i])  # 建立语料库的字典

            line_word = line.split(' ')  # 取出该行语料中的每个词
            line_state = []
            for item in line_word:
                line_state.extend(getList(item))  # 为该行每个字对应一个内部隐状态
            if len(word_list) != len(line_state):
                print(line)
                print(len(word_list), len(line_state))
                print("ERROR:[line_num = %d word_list != line_state]" % line_num)
                break
            else:
                for i in range(len(line_state)):
                    if i == 0:  # 初始状态
                        Pi_dic[line_state[0]] += 1  # Pi_dic记录句子第一个字的状态，计算初始状态概率
                        Count_dic[line_state[0]] += 1  # 记录每一个状态的出现次数
                    else:
                        A_dic[line_state[i - 1]][line_state[i]] += 1  # 计算转移概率
                        Count_dic[line_state[i]] += 1
                        if word_list[i] in B_dic[line_state[i]]:
                            B_dic[line_state[i]][word_list[i]] += 1  # 在字典中，计算发射概率
                        else:
                            B_dic[line_state[i]][word_list[i]] = 0.0  # 不在字典中，加入
        Output()
        input_file.close()
