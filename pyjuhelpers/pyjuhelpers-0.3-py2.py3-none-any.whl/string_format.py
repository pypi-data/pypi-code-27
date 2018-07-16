
def reindent(s, numSpaces, prefix=None):
    _prefix = "\n"
    if prefix:
        _prefix+=prefix

    if not isinstance(s,str):
        s=str(s)
    _str = _prefix.join((numSpaces * " ") + i for i in s.splitlines())
    return _str



def format_columns(data, columns=4, max_rows=4):

    max_len = max( list(map( len, data)))

    cols = max( int(80/max_len),1)

    if columns:
        max_len = 30
    else:
        max_len = max_len

    columns = columns if columns else cols

    my_len = len(data)
    my_len = (my_len - my_len % columns) + columns
    my_range = my_len // columns


    fin_list = [data[i * columns:i * columns + columns] for i in range(my_range)]
    if not max_rows:
        max_rows = len(fin_list)

    sf="{:-^"+str( (columns* (max_len+1))+1)+"}\n"
    s = sf.format(' DATA ')
    for item in fin_list[:max_rows]:
        sf = len(item) * ('|{:^'+str(max_len)+'}')
        sf+="|\n"
        s+=sf.format(*item)
    s+=((columns* (max_len+1))+1) * '-'
    return s

def print_columns(data, columns=4, max_rows=4, indent=2):
    s = format_columns(data, columns=columns, max_rows=max_rows)
    print(reindent(s, indent))