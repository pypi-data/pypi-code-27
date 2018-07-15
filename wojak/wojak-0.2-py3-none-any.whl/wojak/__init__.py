import random
from random import randint
import requests
import json

def get(num=None):
	if num==None:
		req = requests.get("https://yakz.cf/wojaks/wojak.json").json()
		rdmn=randint(0,len(req)-1)
		req=req[rdmn]
		return [req, rdmn]
	argInt = int(num)
	req = requests.get("https://yakz.cf/wojaks/wojak.json").json()
	if(argInt<1 or argInt>len(req)):
		return None

	req=req[argInt-1]
	return [req, argInt]
	
def grayon():
	req = requests.get("https://yakz.cf/wojaks/wojak.json").json()
	return [req[46], 47]