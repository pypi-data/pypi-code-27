import random
from .dictionaries import POKEMONS

def gen(lists = POKEMONS):
    part = random.choice(lists)
    return part

def genarr(count = 1, uniqueList = True, lists = POKEMONS):
    names = []
    for i in range(count):
        name = None
        while not name or (name in names and not uniqueList):
            name = gen(lists)
        names.append(name)
    return names