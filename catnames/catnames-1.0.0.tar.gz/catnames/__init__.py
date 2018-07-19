import random
from .dictionaries import CATS

def gen(lists = CATS):
    part = random.choice(lists)
    return part

def genarr(count = 1, uniqueList = True, lists = CATS):
    names = []
    for i in range(count):
        name = None
        while not name or (name in names and not uniqueList):
            name = gen(lists)
        names.append(name)
    return names