"""this is a simple expriment"""
def print_lol(the_list,indent,leavel=0):
        for each in the_list:
                if isinstance(each,list):
                        print_lol(each,indent,leavel+1)
                else:
                        if indent:
                                for num in range(leavel):
                                        print("\t",end='')
                        print(each)


