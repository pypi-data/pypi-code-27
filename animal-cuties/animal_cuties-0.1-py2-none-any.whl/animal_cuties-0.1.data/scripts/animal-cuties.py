#!python
# -*- coding: utf-8 -*-

import sys

if len(sys.argv) > 2:
    print "too  many arguments"
elif len(sys.argv) < 2:
    print "no arguments given"
else:
    if sys.argv[1]=="cat" or sys.argv[1]=="kitty":
        print("=(^o ω o^)= <3 meow!")
    elif sys.argv[1]=="dog" or sys.argv[1]=="puppy":
        print("U(o . o)U <3 woof!")
    elif sys.argv[1]=="rabbit" or sys.argv[1]=="bunny":
        print("|(u x u)| <3 *snuffles*")
    else:
        print "I don't know that animal"
