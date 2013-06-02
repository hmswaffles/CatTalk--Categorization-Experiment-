import pygame
import random
from itertools import product
import math
import os

def dualtaskgenerator(numb_white):
    DUAL_DIR = 'C:\Users\Evan\Desktop\experiment_code\Dual'
    DUALSQ=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    DUALNWHITE=numb_white
    TOTAL_N=19

    margin = 10
    height = 40
    width = 40

    size = [255, 255]




    
    #shuffled numbers, for (pre)deterministic n back task
    Shuff_1 = [11, 2, 9, 18, 17, 25, 22, 7, 21, 6, 24, 8, 13, 19, 14, 5, 1, 3, 15, 12, 10, 20, 4, 16, 23]
    Shuff_2 = [2, 8, 14, 23, 19, 24, 22, 5, 7, 10, 6, 3, 1, 21, 20, 18, 16, 17, 25, 12, 4, 13, 15, 11, 9]
    Shuff_3 = [6, 3, 12, 5, 1, 8, 20, 24, 17, 4, 25, 10, 16, 2, 18, 22, 23, 13, 7, 9, 15, 14, 19, 11, 21]
    Shuff_4 = [18, 6, 24, 14, 8, 16, 1, 10, 5, 15, 7, 20, 17, 21, 4, 19, 11, 12, 23, 2, 9, 22, 13, 25, 3]
    Shuff_5 = [5, 22, 14, 11, 12, 16, 21, 6, 18, 10, 9, 17, 20, 25, 15, 23, 1, 24, 3, 8, 13, 19, 4, 7, 2]
    Shuff_6 = [10, 4, 20, 24, 5, 16, 23, 15, 14, 1, 22, 9, 6, 12, 13, 3, 21, 19, 7, 2, 25, 17, 8, 18, 11]
    Shuff_7 = [16, 3, 25, 18, 5, 19, 15, 2, 1, 17, 24, 8, 20, 4, 11, 23, 9, 6, 13, 21, 22, 14, 12, 10, 7]
    Shuff_8 = [21, 15, 11, 9, 3, 14, 25, 20, 1, 5, 12, 16, 23, 6, 19, 4, 2, 8, 13, 7, 22, 17, 18, 24, 10]
    Shuff_9 = [24, 7, 13, 23, 15, 16, 14, 4, 20, 8, 10, 3, 17, 21, 25, 11, 18, 12, 22, 9, 5, 1, 2, 6, 19]
    Shuff_10 = [21, 7, 23, 2, 13, 3, 25, 14, 16, 19, 1, 9, 4, 5, 22, 11, 17, 12, 8, 15, 18, 20, 24, 10, 6]
    Shuff_11 = [7, 6, 23, 3, 9, 17, 13, 8, 18, 11, 22, 12, 4, 2, 24, 10, 1, 20, 25, 16, 21, 15, 14, 19, 5]
    Shuff_12 = [22, 19, 17, 25, 9, 6, 14, 20, 5, 4, 18, 3, 24, 1, 2, 23, 7, 11, 10, 21, 15, 12, 16, 13, 8]
    Shuff_13 = [25, 19, 8, 10, 7, 13, 21, 3, 6, 1, 15, 17, 20, 2, 5, 4, 14, 16, 22, 12, 18, 11, 24, 9, 23]
    Shuff_14 = [24, 5, 17, 6, 22, 2, 1, 9, 3, 15, 20, 23, 18, 11, 14, 21, 8, 25, 16, 12, 4, 13, 7, 10, 19]
    Shuff_15 = [20, 4, 11, 9, 6, 19, 14, 18, 12, 17, 10, 24, 16, 25, 3, 22, 7, 2, 13, 8, 23, 21, 1, 15, 5]
    Shuff_16 = [16, 7, 1, 9, 2, 8, 24, 5, 13, 25, 19, 14, 21, 4, 6, 12, 11, 22, 23, 18, 17, 10, 20, 15, 3]
    Shuff_17 = [14, 7, 16, 12, 6, 15, 17, 19, 3, 21, 25, 11, 13, 23, 10, 9, 1, 5, 8, 22, 20, 18, 4, 2, 24]
    Shuff_18 = [22, 4, 25, 16, 19, 2, 24, 13, 14, 9, 15, 1, 5, 7, 8, 20, 11, 23, 18, 17, 12, 10, 3, 21, 6]
    Shuff_19 = [5, 17, 21, 8, 4, 13, 15, 3, 14, 9, 22, 6, 16, 18, 24, 25, 1, 11, 7, 12, 20, 23, 10, 2, 19]
    
    Master_ls = [Shuff_1,Shuff_2,Shuff_3,Shuff_4,Shuff_5,Shuff_6,Shuff_7,Shuff_8,Shuff_9,Shuff_10,Shuff_11,Shuff_12,Shuff_13,Shuff_14,Shuff_15,Shuff_16,Shuff_17,Shuff_18,Shuff_19]




    
    random.shuffle(Master_ls)
    dual_task_rect_ls = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]



    for j in range(0,18):
            whitecount =0
            pattern=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            color=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            a=Master_ls[j]
            b=a[0:12]
            b.sort()
            b=b+[0,0,0,0,0,0,0,0,0,0,0,0,0]
          
            for i in range(0,24):
                if i in b:
                    pattern[i]=1
                    whitecount +=1
                else:
                    pattern[i]=0
            for k in range(0,25):
                if pattern[k]:
                    color[k] = (254,254,254)
                else:
                    color[k]= (0,0,0)
            dual_task_rect_ls[j] = color

    #now ready to draw the images and save them with pygame.
    print 'pre'
    pygame.init()


    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    while done == False:
        
        #print 'pygame'
        for im_numb in range(0,18):
            size = [255, 255]
            screen=pygame.display.set_mode(size)
            pygame.time.wait(500)
            print im_numb
            screen.fill((0,0,0))
            pygame.display.flip
            a = dual_task_rect_ls[im_numb] # a is the list of colors
            for square in range(0,24):
                pygame.time.wait(100)
                row=math.floor(square/5)
                if square<5:
                    column=square
                else:
                    column= square-5*row
                pygame.draw.rect(screen,a[square],[(margin+width)*column+margin, (margin+height)*row+margin, width, height])
                pygame.display.flip            
            pygame.image.save(screen,os.path.join(DUAL_DIR, str(im_numb)+'.png'))
            if im_numb== 17:
                done = True
        
    #    for event in pygame.event.get(): # User did something
    #        if event.type == pygame.QUIT: # If user clicked close
    #            done = True # Flag that we are done so we exit this loop




    
    # Set the height and width of the screen
    
          

            
