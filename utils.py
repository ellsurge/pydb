import random, string

VAR ='varchar(255)'
TEXT = 'TEXT' 
INT  = 'INT'
BOOL = 'BOOLEAN'
LONG  = 'LONG INT'
PK = 'PRIMARY KEY'
ID  ='id'


    
global mode 
mode ='dev'

def rnd_str_gen(len):
    pass
    
def keygen (string):
    
    pass
def is_int(i):
    try:
        int(i)
    except:
        return True
    else:
        return False

def s_x(s, num):
    n =0
    a = []
    while n <num:
        a.append(s)
        n = n +1
    return a
       
    
def par(s):
    s = str(s)
    return '('+s+')'  
 
def qoute(s, p =0):
    s = str(s)
    if(p is 0):
        return '`'+s+'`'  
    else:
        return '\''+s+'\''  
def qoute2(s):
    s = str(s)
    return '\''+s+'\''
def sub_arr(dic, field):
    arr  = list()
    for ell in dic:
        arr.append(ell[field])
    return arr
       
def stringify(ell, div=' ', top ='', end='', key = False,value= False, mid = ' ' ):
    txt= top
    if (type(ell) is list or type(ell) is tuple):
        n=1
        for word in ell:
            word  = str(word)
            if(value):
                word = value(word)
            if(n <len(ell)):
                txt +=  word+div
            else:
                txt +=  word
            n = n+1

    elif (type(ell) is dict):
        n =1
        for x,y in ell.items():
            x,y = str(x), str(y)
            if(key):
                x = key(x)
            if(value):
                y = value(y)
            if(n < len(ell)):
                txt += x+mid+y+div
            else:
                txt += x+mid+y
            n= n+1   

    txt += end
    return txt

def log(message):
    if(mode == 'dev'):
        print('log: ')
        print(message)
        