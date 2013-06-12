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

def Dual_order_gen_alt1(m):# for n-back ==1, m is blocks of 30, so m ==10 would yield a list 300 items long
    master_ls=[]
    for k in range(0,m):
        order_ls = []
        a = range(0,15)
        random.shuffle(a)
        b = a[0:3]
        aa = a[3:]
        bb = a[3:]
        random.shuffle(aa)
        random.shuffle(bb)
        #check to make sure the inner boarders aren't the same
        #check to make sure that the m boarders aren't the same
        z = bb+aa
        
        for i in range(0,3):
            d = random.randint(0,8)
            
            for j in range(0,8):
                if j == d:
                    numb =  [b[i],b[i]]
                else:
                    index = j*(i+1)
                    numb = z[index]
                    
                order_ls.append(numb)
              
                
        master_ls.append(order_ls)
        
    return flatten(master_ls)

def Dual_order_gen_alt2(m):# for n-back ==2, m is blocks of 30, so m ==10 would yield a list 300 items long
    master_ls=[]
    flag = False
    altflag = False
    for k in range(0,m):
        print 'k',k
        order_ls = []
        a = range(0,15)
        random.shuffle(a)
        b = a[0:3]
        aa = a[3:]
        bb = a[3:]
        random.shuffle(aa)
        random.shuffle(bb)
        z = bb+aa
        f = [0,1,2,3,4,5,6,7,8]
        
        for i in range(0,3):
            d = random.sample(f,3)
            for j in range(0,8):
                index = j*(i+1)

                
                if j == d[i]:
                    numb =  [b[i],z[index],b[i]]
                    flag = True
              #  elif flag:
              #      flag = False
              #      altflag = True
              #      pass
              #  elif altflag:
              #      altflag= False
              #      pass
                else:

                    numb = z[index]
                    
                order_ls.append(numb)
              
                
        master_ls.append(order_ls)
        
    return flatten(master_ls)s
                

def flatten(l):#list flattener
  out = []
  for item in l:
    if isinstance(item, (list, tuple)):
      out.extend(flatten(item))
    else:
      out.append(item)
  return out        
        
                
            


