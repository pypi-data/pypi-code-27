import random
from .dictionaries import WORDLIST

def genword(lists = WORDLIST):
    part = random.choice(lists)
    return part
