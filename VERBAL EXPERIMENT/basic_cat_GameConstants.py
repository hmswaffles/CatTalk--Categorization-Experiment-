import math
import pygame
import sys
import os
from pygame.locals import *
import random

#Initialize Pygame
pygame.init()
#Set Mouse to not show
#pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

#Define Screen Size
if os.name == 'nt': # are we running Windows?
    screen = pygame.display.set_mode((1024,768),FULLSCREEN)
    FULL_SCREEN = True
else:
    screen = pygame.display.set_mode((1024,768))
    FULL_SCREEN = False
x, y = screen.get_size()
#Define Screen Size
SCREEN_SIZE = (x,y)
SCREEN_RECT = ((0,0),(0,SCREEN_SIZE[1]),SCREEN_SIZE,(SCREEN_SIZE[1],0)) #Defines coordinates of the screen
SCREEN_CENTER = (SCREEN_SIZE[0]/2,SCREEN_SIZE[1]/2)

#This will  make the game be in the center of the screen
GAME_SIZE = (x,y)
one = (SCREEN_CENTER[0] - GAME_SIZE[0]/2, SCREEN_CENTER[1] - GAME_SIZE[1]/2)
two = (SCREEN_CENTER[0] - GAME_SIZE[0]/2, SCREEN_CENTER[1] + GAME_SIZE[1]/2)
three = (SCREEN_CENTER[0] + GAME_SIZE[0]/2, SCREEN_CENTER[1] + GAME_SIZE[1]/2)
four = (SCREEN_CENTER[0] + GAME_SIZE[0]/2, SCREEN_CENTER[1] - GAME_SIZE[1]/2)
GAME_RECT = (one,two,three,four)


BACKGROUND_COLOR = (120,120,120)          #Background screen color
SAMPLING_RATE = 100

#Game timing info
FIXATION_TIME = 1
REACTION_TIMEOUT_1 = 3.0
REACTION_TIMEOUT_2 = 3.0
FEEDBACK_TIME = 3.0
ITI_TIME = 0.5
BLOCKFB_TIME = 5.0
SCORE_COLOR = (0,0,0)
MAX_STIMULI_PRESENTATION_TIME = 4.0

#Filename directories
TRIALSET_DIR = 'C:\Users\Evan\Desktop\experiment_code\VERBAL EXPERIMENT\TargetFiles'
DATA_DIR = 'C:\Users\Evan\Desktop\experiment_code\VERBAL EXPERIMENT\Data'
STIMULI_DIR = 'C:\Users\Evan\Desktop\experiment_code\VERBAL EXPERIMENT\Stimuli'
#DUAL_DIR = 'C:\Users\Evan\Desktop\experiment_code\Dual\'
#Variables in Trial File
TRIAL_NUM = []
CAT = []
LENGTH = []
THETA = []
BETWEEN_BLOCKS = []

#Need this list for the user input window
LETTERS = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
           "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
NUMBERS = ["0","1","2","3","4","5","6","7","8","9","_"]


#N-back
N=0
Numbs = [1,2,3,4,5,6,7,8,9]
Fontsizes = [54,68,46,72,120,140,150]
disp_ls=[]
DUAL_DISP_TIME =3
DUALFLAG=True

DUALSQ=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
DUALNWHITE=13
TOTAL_N=15
DUALCOUNTER=0
DUALCOUNT=0

#dimensions of white spatial grid bits:
DTwidth = 20
DTheight = 20 
DTmargin = 5 # This sets the margin between each cell


Dualorder1=[8, 5, 3, 2, 0, 6, 10, 9, 9, 8, 3, 0, 10, 4, 14, 6, 1, 1, 11, 11, 2, 10, 13, 6, 7, 10, 14, 10, 14, 8, 1, 9, 4, 7, 7, 12, 10, 8, 9, 5, 2, 2, 6, 13, 1, 10, 1, 5, 3, 13, 0, 0, 11, 5, 8, 6, 14, 4, 3, 9, 10, 11, 8, 14, 3, 10, 1, 1, 13, 3, 11, 8, 4, 10, 5, 5, 3, 12, 10, 4, 5, 11, 1, 0, 14, 3, 3, 2, 12, 5, 1, 14, 2, 7, 9, 12, 8, 5, 0, 4, 4, 6, 12, 6, 11, 1, 12, 2, 9, 3, 3, 14, 6, 11, 7, 12, 9, 14, 11, 10, 0, 0, 7, 13, 12, 13, 11, 5, 7, 1, 1, 9, 8, 14, 8, 13, 1, 12, 3, 7, 4, 4, 14, 13, 12, 7, 0, 10, 10, 0, 13, 14, 1, 7, 9, 9, 0, 1, 14, 3, 8, 7, 3, 10, 5, 5, 14, 1, 2, 8, 3, 12, 1, 4, 4, 6, 3, 8, 8, 10, 1, 13, 13, 3, 9, 10, 6, 11, 7, 5, 6, 4, 10, 14, 1, 1, 11, 5, 4, 14, 3, 9, 9, 3, 8, 11, 6, 14, 13, 3, 0, 0, 14, 2, 13, 2, 9, 0, 5, 8, 1, 6, 6, 10, 10, 9, 5, 1, 11, 12, 11, 8, 13, 14, 14, 1, 3, 11, 7, 13, 5, 13, 13, 11, 2, 4, 6, 9, 14, 5, 1, 2, 6, 7, 7, 12, 3, 9, 0, 1, 4, 14, 8, 10, 10, 2, 8, 3]
#>>> dual_tester(a,1)
#0.10820895522388059
#generated with Dual_order_gen_alt1

Dualorder2= [11, 3, 9, 0, 2, 0, 13, 4, 12, 6, 11, 9, 10, 13, 10, 12, 7, 1, 4, 11, 11, 2, 12, 8, 5, 4, 5, 13, 2, 6, 13, 4, 9, 12, 2, 12, 0, 10, 5, 7, 13, 9, 0, 5, 11, 8, 7, 1, 0, 1, 13, 2, 5, 14, 7, 3, 5, 3, 14, 8, 7, 5, 14, 6, 14, 8, 13, 2, 12, 0, 7, 6, 1, 13, 1, 12, 3, 10, 6, 2, 7, 8, 12, 11, 4, 6, 4, 12, 5, 7, 12, 4, 13, 1, 6, 1, 14, 7, 3, 0, 12, 13, 14, 3, 11, 10, 11, 8, 10, 9, 12, 6, 3, 5, 10, 5, 12, 2, 0, 2, 13, 9, 11, 1, 14, 12, 4, 8, 2, 8, 13, 0, 11, 0, 14, 4, 10, 5, 7, 12, 13, 1, 3, 4, 3, 6, 7, 11, 4, 5, 14, 3, 1, 9, 1, 10, 6, 5, 11, 12, 14, 9, 6, 11, 4, 7, 0, 7, 10, 9, 14, 10, 11, 2, 13, 2, 10, 4, 8, 0, 8, 3, 4, 3, 2, 7, 11, 0, 5, 14, 8, 2, 11, 9, 5, 9, 12, 1, 5, 2, 10, 8, 10, 7, 5, 6, 5, 0, 11, 7, 3, 11, 2, 0, 7, 0, 13, 5, 1, 6, 3, 2, 14, 13, 14, 1, 12, 8, 7, 12, 3, 7, 1, 9, 7, 13, 4, 6, 4, 10, 10, 0, 7, 2, 9, 13, 9, 3, 6, 5, 10, 7, 13, 6, 12, 14, 3, 4, 2, 4, 10, 2, 6, 8, 1, 8, 3, 7, 12, 13, 8, 6, 0, 7, 9, 10, 9, 12, 13, 14, 8, 0, 10, 4, 13, 4, 3, 2, 13, 14, 8, 7, 13, 11, 13, 5, 8, 1, 10, 1]
#>>> dual_tester(a,2)
#0.11333333333333333

#Dual Trainnig
training_total_runs = 6 #this is twice the number of  the minimum trial n-back presentations

DTtrainingorder = [11, 3, 9, 9, 9, 2, 0, 13, 4, 12, 6, 6, 6, 11, 9, 10, 13, 10, 12, 7, 1, 4, 11, 1,  7, 10, 14, 10, 14, 14, 8, 1, 9, 4, 7, 7, 12, 10, 8, 9 ]



#Instruction Text
INSTRUCTIONTEXT= """INSTRUCTIONS: \n You will be presented with a series of lines drawn from two different categories. \n
Your mission, should you choose to accept it, is to figure out the categories- lines can be classified by pressing either 'k' or 'd' 
\n Be sure to be quick about it, or a time penalty will be enforced. \n There is also a secondary, concurrent task which the RA will explain.
"""
