import sys
if len(sys.argv) != 2:
      sys.exit('wrong number of arguments')
filename= sys.argv[1]

old = ''
newLine = True
insideLiteral = False
with open(filename) as f:
    #while True:
    #    c = f.read(1)
    for line in f: 
        newLine = True
        insideLiteral = False
        for c in line:
            if c != ' ':
                newLine = False
            if c == '\'' and line[0] != '#':
                insideLiteral = not insideLiteral    
            if old != ' ' or insideLiteral:
                print(old,end='')
            elif(newLine):
                print(old,end='')
            elif(c not in [' ',',']):
                print(old,end='')
            if (old=='\\' and c in ['u','r','f','n','e','a','b'] and not  insideLiteral):
                print('\\',end='')
            old=c

    print(old,end='')
