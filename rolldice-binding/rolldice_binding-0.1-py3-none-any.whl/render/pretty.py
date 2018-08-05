import time
from shutil import get_terminal_size

def render(results, args):
    console_width = get_terminal_size((80,48)).columns

    # print each section
    for r in results:
        header_prefix = '# '+r[0]+' '
        print(header_prefix + '#'*(console_width - len(header_prefix)))
        print(' '+r[2])
        print(' ->', r[1])
        print()
    
    # print tail
    tail_suffix = time.strftime(' %H:%M:%S ###')
    print('#'*(console_width - len(tail_suffix)) + tail_suffix)
