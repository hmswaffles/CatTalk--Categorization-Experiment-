import pygame
import os,sys

def verbal_dual(wordparameter):
    """
generates the words for the verbal interefernce dual task. if wordparameter is
    false, then is uses the fake words for control

    """

    
    Verbal_DIR = 'C:\Users\Evan\Desktop\experiment_code\Verbal'


     #from random.org/strings
    if wordparameter== 'space':
        words = ['thick','thin','straight','curve','border','edge','space','dimension','dash','dot','position','location','solid','narrow','wide']
    elif wordparameter == 'color':
        words = ['red','orange','green','teal','yellow','ochre','mauve','blue','orange','brown','pink','magenta','purple','cerulean','celedon']
    elif wordparameter == 'unique_nonce':
        words = ['EKPOUVS', 'RQNJABK','IJWORSC','VFOLPEN','DQEIWEJ','GYPNKRC','WGELQOB','LDPWAMK','NQCPOWW','XHHHGTR','KTJDWBH','BMSRCFX','UWJTUFZ','WSCBVTJ','CHDGUDG']
    else:
        print 'add new 15 word list and edit paramter on line 42'
    
    pygame.init()

    font = pygame.font.Font('C:\\Windows\\Fonts\\georgia.ttf', 54)

    
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    while done == False:
        
        #print 'pygame'
        for word_numb in range(0,15):
            
            pygame.time.wait(100)
            size = [255, 255]
            screen=pygame.display.set_mode(size)
            pygame.time.wait(300)
            print word_numb
            screen.fill((120,120,120))
            background = pygame.Surface(screen.get_size())
            #background = background.convert()
            background.fill((120, 120, 120))
            
            
            a = words[word_numb] #a is now the list of words, specified above
            b = font.render(a,1,(245,245,245))
            bpos = b.get_rect()
            bpos.centerx = background.get_rect().centerx
            bpos.centery = background.get_rect().centery
            screen.blit(b, bpos)
            pygame.display.flip
                
            pygame.image.save(screen,os.path.join(Verbal_DIR, str(word_numb)+'.png'))
            if word_numb== 14:
                done = True
                pygame.display.quit()   #Closes the display
                sys.exit()




