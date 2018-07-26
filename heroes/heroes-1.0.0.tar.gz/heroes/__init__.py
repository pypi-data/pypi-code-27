import random
from .dictionaries import WORDLIST

def gen(lists = WORDLIST):
    part = random.choice(lists)
    return part

def genarr(count = 1, uniqueList = True, lists = WORDLIST):
    names = []
    for i in range(count):
        name = None
        while not name or (name in names and not uniqueList):
            name = gen(lists)
        names.append(name)
    return names