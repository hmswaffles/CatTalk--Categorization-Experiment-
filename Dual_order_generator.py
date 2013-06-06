from __future__ import division
import random


def Dual_order_gen(n): #generates this list for order of dual task presentation
    numb = []
    for i in range(0,360):

        #begin 10% section
        if random.randint(0,8+n*2) == 0:
            nextnumb = numb[i-n]
        else:
            nextnumb = random.randint(1,15)
        numb.append(nextnumb)
    return numb
            
def dual_tester(listnumb,n):#when its around 10%, I'll copy it into catgameconstants
    total = 0 
    for i in range(len(listnumb)):
        if listnumb[i] == listnumb[i-n]:
            count = 1
           #print 'another!'
        else:
            count = 0
        total = total + count
    return total/len(listnumb)


