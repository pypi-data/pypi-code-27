"""this is a simple expriment"""
def print_LOL(the_list):
	for each in the_list:
		if isinstance(each,list):
			print_lol(each)
		else:
			print(each)
