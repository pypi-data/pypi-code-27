# rkpython
# Python module containing various functions for personal use

# dependencies
import os
import operator
import sys

# rk.to_txt()
def to_txt(l, path = 'text_file.txt', overwrite = False, verbose = False):

#Docstring
    '''
    Saves a list to a .txt file.

    --------------
    
    l : list, default is None
        List object to be saved.  
    
    path : str, default is 'text_file.txt'
        File path (with file name) you want to save to.  
    
    overwrite : bool, default is False  
        Overwrites the file if it exists.
        
    verbose : boolean, default is False
        Prints out a message if the operation was succesful
        
    --------------

    Examples :
    
    rk.to_txt(var_list, './documents/vars.txt', verbose = True)
    >> File successfully written to ./documents/vars.txt
    '''
    
    if type(l) == list:
        if overwrite == True:
            try: 
                with open(path, 'w') as file:
                    for obj in l:
                        file.write("%s\n" % obj)
                if verbose == True :
                    print(f'File successfully written to {path}')
            except:
                if os.access(path, os.W_OK) == False:
                    raise ValueError(f"No write permissions for the file : {path}. Verify that the file isn't used by another program")
                else:
                    raise ValueError(f"Could not access the file : {path}")

        elif os.path.isfile(path):
            raise ValueError(f"File already exists : {path}. Try overwite = True.")
        else :
            try: 
                with open(path, 'w') as file:
                    for obj in l:
                        file.write("%s\n" % obj)
                    if verbose == True :
                        print(f'File successfully written to {path}')
            except:
                raise ValueError(f"Could not write on file : {path}")
    else :
        raise ValueError(f"Parameter l is not a list")
        
# rk.read_txt()
def read_txt(path = 'text_file.txt', verbose = False):

#Docstring
    '''
    Reads from a text file, saving the result as a list, where each line is one item.
    
    --------------
    
    path : str, default = 'text_file.txt'
        File path (with file name) you want to read from. Can be any type of file (.txt, .csv...)  
    
    verbose : boolean, default is False
        Prints out a message if the operation was succesful
        
    --------------

    Examples :
    
    var_list = rk.read_txt('./documents/vars.txt', verbose = True)
    >> File successfully read from ./documents/vars.txt
    '''
    
    if os.access(path, os.R_OK) == False:
        raise ValueError(f"No read permissions for the file : {path}. Verify that the file exists")
    else:
        with open(path) as file:
            l = file.read().splitlines()
            if verbose == True :
                    print(f'File successfully read from {path}')
            return l
			
# rk.to_size()
def to_size(size_in_bytes):

#Docstring
    '''
    Converts a number of bytes into a more readable unit, up until Terabytes, and rounds the number down to 1 decimal. Returns a string.
    
    --------------
        
    size_in_bytes : int
        Size in bytes that needs to be converted
        
    --------------

    Examples :
    
    get_size(124480000)
    >> '124.5 Mb'
    '''
    if type(size_in_bytes) not in [int, float]:
        raise ValueError('Expected a float or integer.')
    else :
        power = 0
        while (abs(size_in_bytes) > 700) & (power < 4):
            size_in_bytes = size_in_bytes/1000
            power += 1

        if power == 0:
            power = 'Byte'
        elif power == 1:
            power = 'Kb'
        elif power == 2:
            power = 'Mb'
        elif power == 3 :
            power = 'Gb'
        elif power == 4 :
            power = 'Tb'
        else :
            power = '[Error in determining size]'

        return_str = f'{round(size_in_bytes, 1)} {power}'
        return return_str
		
# rk.get_mem()
def get_mem(nb_objects = 10):

#Docstring
    '''
    Prints out a list of the largest objects stored in memory, as well as the total memory usage of global variables. Returns a string.
    
    --------------
        
    nb_objects : int, default =  10
        Maximum number of items to be printed out.
        
    --------------

    Examples :
    
    get_mem(5)
    >> Total usage : 25.3 Gb
    >>
    >>  5 largest objects :
    >>  _477  :  1.7 Gb
    >>  _529  :  1.7 Gb
    >>  _437  :  1.4 Gb
    >>  _412  :  1.3 Gb
    >>  _415  :  1.3 Gb
    '''
    if type(nb_objects) != int:
        raise ValueError('Expected an integer.')
    elif  nb_objects < 0:
        raise ValueError('nb_objects needs to be positive')
    else:
        obj_dict = {}
        for var in globals():
            try: 
                obj_dict[var] = sys.getsizeof(eval(var))
            except:
                pass

        sorted_dict = sorted(obj_dict.items(), key=operator.itemgetter(1), reverse=True)

        mem_total = sum(obj_dict.values())

        mem_total = to_size(mem_total)

        print(f'Total usage : {mem_total}')
        nb_objects = min(nb_objects, len(sorted_dict))

        print(f'\n{nb_objects} largest objects :')
        for i in range(nb_objects):
            print(sorted_dict[i][0], ' : ', to_size(sorted_dict[i][1]))