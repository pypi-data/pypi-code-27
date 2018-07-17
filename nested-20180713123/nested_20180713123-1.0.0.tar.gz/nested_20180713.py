def print_lol(the_list):
	      for nested_item in the_list:
		      if isinstance(nested_item,list):
			      print_lol(nested_item)
		      else:
			      print(nested_item)