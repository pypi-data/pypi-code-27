import random
from .dictionaries import MALE, FEMALE

def male(lists = MALE):
    part = random.choice(lists)
    return part

def malearr(count = 1, uniqueList = True, lists = MALE):
    names = []
    for i in range(count):
        name = None
        while not name or (name in names and not uniqueList):
            name = male(lists)
        names.append(name)
    return names


def female(lists = FEMALE):
    part = random.choice(lists)
    return part

def femalearr(count = 1, uniqueList = True, lists = FEMALE):
    names = []
    for i in range(count):
        name = None
        while not name or (name in names and not uniqueList):
            name = female(lists)
        names.append(name)
    return names