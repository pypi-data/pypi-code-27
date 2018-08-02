#  ----------------------------------------
#   This script turns comments into docstrins
#   By: Quinn
#   Started on: 5/10/18
#-------------------------------------------

import sys
if len(sys.argv) != 2:
      sys.exit('wrong number of arguments')
fname= sys.argv[1]


# ---------------------
#    Read from file
# --------------------

def math_highlight(inline):
    n = inline.count('$')
    if n < 2:
        return inline
    out = ''
    mathmode=False
    for c in inline:
        if c == '$':
            if mathmode:
                out=out+'`'
                mathmode=False
            else:
                out=out+':math:`'
                mathmode=True
        else:
            out=out+c
    return out

buf = []
defopen = False
count = 0
mathmode = False
nalign=[0,0]
with open(fname) as f:
    for line in f:
        count = count+1
        if line[0] is '#':
            if line[0:5] == '# In[':
                continue
            if line[0:4] == '# # ':
                print('# ============================================================ #')
                print('#')
                print(line,end='')
                print('#')
                print('# ============================================================ #')
                continue
            if line[0:5] == '# ## ':
                print('# --------------------------------------------------- #')
                print(line,end='')
                print('# --------------------------------------------------- #')
                continue
            if line[0:5] == '# ###':
                print(line,end='')
                print('#_____________________________#')
                continue
            buf.append(line[1:])
        else:
            print(line,end='')
            if line[0:4] == 'def ':
                defopen = True

            if defopen and ':' in line:
                print('    """')
                for x in buf:
                    if '$$' in x:
                        if not mathmode:
                            mathmode=True
                            print('    .. math::')
                            continue
                        else:
                            mathmode=False
                            continue
                    if '\[' in x:
                        if mathmode:
                            raise ValueError(' got an unexpected \[')
                        else:
                            mathmode=True
                            print('    .. math::')
                            continue

                    if 'begin{align' in x:
                        if mathmode:
                            raise ValueError(' got an unexpected \begin{align')
                        else:
                            mathmode=True
                            nalign[0]=nalign[0]+1
                            print('    .. math::')
                            continue

                    if '\]' in x:
                        if not mathmode:
                            raise ValueError(' got an unexpedted \]')
                        mathmode = False
                        continue
                    if '\end{align' in x:
                        if not mathmode:
                            print(nalign)
                            raise ValueError(' got an unexpedted \end{align')
                        nalign[1]=nalign[1]+1
                        mathmode = False
                        continue


                    if mathmode or '$$' in x:
                        if mathmode and x[-2] == '\\':
                            print('       '+x[0:-3]+' \\\\\\\\')
                        else:
                            print('       '+x)

                    else:
                        print('   '+math_highlight(x))


                buf=[]
                print('    """')
                defopen=False

       
        
