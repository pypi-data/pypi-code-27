#python3
#inspired by Dr.Kingshuk Chatterjee
#this package includes PyAvroPhonetic by kaustavdm as installing it via pip does not work properly
#Also requires pyenchant
globstr=""
def conv(stre="",delim="!?.",n=0):
    '''convert bengali text written in english to bengali while keeping english ony text '''
    import string#importing string
    from pyavrophonetic import avro
    import enchant
    d = enchant.DictWithPWL("en_GB","data/bdict4.txt")
    strret=""
    english=0
    bengali=0
    startendsign=""
    global globstr
    try:
        while stre[n]!="." and stre[n]!="?" and stre[n]!="!":
            # Iterating from the back of the sentence
            strret+=stre[n]
            n += 1
        else:
          endendsign=stre[n]  
    except:
        return "Done"
    strlst=strret.split()
    lenghty=len(strlst)
    for element in range(lenghty):
        flag1=0
        flag2=0
        if d.check(strlst[element]):
            flag1+=1
        elementben=avro.parse(strlst[element])
        if d.check(elementben):
            flag2+=1
        if flag1==1 and flag2==0:
            english+=1
        elif flag1==0 and flag2==1:
            bengali+=1
        elif flag1==1 and flag2==1:
            english+=1
            bengali+=1
        else:
            pass
    if english>bengali:
        pass
        strret=" ".join(strlst)
    elif bengali>english:
        for element in range(lenghty):
            flag1=0
            flag2=0
            if d.check(strlst[element]):
                flag1+=1
            elementben=avro.parse(strlst[element])
            if d.check(elementben):
                flag2+=1
            if flag1==1 and flag2==0:
                pass
            elif flag1==0 and flag2==1:
                strlst[element]=elementben
            elif flag1==1 and flag2==1:
                pass
            else:
                pass
            
        strret= " ".join(strlst)
    else:
        pass
    strret=startendsign+strret+avro.parse(endendsign)
    print (strret,)
    globstr+=strret
    conv(stre,n=n+1)
    
def call(str1):
    '''Function to send converted text to file converter'''
    global globstr
    globstr=""
    conv(str1)
    return globstr

#Usage: conv("Folder zip korte hobe abar . ami korbo.")

def callfileconvert():
    '''Driver function for converting files'''
    while True:
        flname=input("Enter txt file name:")
        with io.open(flname,'r',encoding='utf8') as opf:
                   text11 = opf.read()
        rettxt=call(str1=text11)
        with io.open(flname+"-converted.txt",'w',encoding='utf8') as opf:
                   opf.write(rettxt)
        print("Done converting an saved in file:",flname,"-coverted.txt")
        choi=input("Enter choice(1-Continue/0-Abort):")
        if choi=="0":
            print("Closing....")
            break
        else:
            pass
    
conv("Folder zip korte hobe abar . ami korbo.")
