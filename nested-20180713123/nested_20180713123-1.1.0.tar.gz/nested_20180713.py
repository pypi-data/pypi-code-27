def print_lol(the_list,level):
	      for nested_item in the_list:
		      if isinstance(nested_item,list):
			      print_lol(nested_item,level)
		      else:
				  for tab_stop in  range(level):
					  print("\t",end='')
			      print(nested_item)