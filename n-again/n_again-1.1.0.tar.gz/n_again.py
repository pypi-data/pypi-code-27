"""this is a simple expriment"""
ddef print_lol(the_list,leavel):
        "version=1.1.0，leael参数可以控制输出缩进"
	for each in the_list:
		if isinstance(each,list):
			print_lol(each,leavel+1)
		else:
			for num in range(leavel):
				print("\t",end='')
			print(each)

