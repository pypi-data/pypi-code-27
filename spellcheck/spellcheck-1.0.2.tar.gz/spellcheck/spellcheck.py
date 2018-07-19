from nltk.corpus import words
import jellyfish
import itertools
def fix(word):
    word_list = words.words(lang='es')
    score=0
    op=[]
    bst=[]
    bst2=[]
    ind=''
    opl=[]
    nope=[]
    done={}
    for x in range(len(word_list)):
        if jellyfish.jaro_distance(word, word_list[x]) > score:
            score=jellyfish.jaro_distance(word, word_list[x])
            op=(word_list[x])
            opl.append(score)
            bst.append(score)
            bst2.append(word_list[x])
        if jellyfish.jaro_distance(word, word_list[x]) == score:
            bst.append(score)
            bst2.append(word_list[x])
    for x in range(len(bst)):
        done[x+bst[x]]=bst2[x]

    for x in range(len(bst)):
        gog=bst[x]
        if str(score) in str(gog):
            nope.append(bst2[x])
    nope=list(set(nope))
    return(nope[0])
