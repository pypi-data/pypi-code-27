def print_lol(the_list,level=0):
	for nested_item in the_list:
		if isinstance(nested_item,list):
			print_lol(nested_item,level+1)
		else:
			for tab_stop in range(level):
				print("\t",end='')
			print(nested_item)