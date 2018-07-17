def print_lol(the_list,indent = False,level=0):
	for nested_item in the_list:
		if isinstance(nested_item,list):
			print_lol(nested_item,indent,level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end='')
			print(nested_item)