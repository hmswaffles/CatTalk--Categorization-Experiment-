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


BACKGROUND_COLOR = (0,0,0)          #Background screen color
SAMPLING_RATE = 100

#Game timing info
FIXATION_TIME = 0.9
REACTION_TIMEOUT_1 = 2.0
REACTION_TIMEOUT_2 = 2.0
FEEDBACK_TIME = 2.0
ITI_TIME = 0.5
BLOCKFB_TIME = 5.0
SCORE_COLOR = (255,255,255)

#Filename directories
TRIALSET_DIR = 'C:\Users\Evan\Desktop\experiment_code\TargetFiles'
DATA_DIR = 'C:\Users\Evan\Desktop\experiment_code\Data'
STIMULI_DIR = 'C:\Users\Evan\Desktop\experiment_code\Stimuli'
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
DUAL_DISP_TIME =1.4
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



Dualorder1=[6, 8, 11, 7, 8, 8, 3, 1, 1, 8, 8, 14, 12, 4, 10, 3, 3, 14, 1, 11, 6, 15, 15, 5, 8, 10, 1, 10, 10, 2, 12, 10, 9, 12, 3, 2, 8, 11, 2, 4, 10, 9, 12, 7, 3, 1, 14, 15, 10, 13, 15, 2, 4, 9, 2, 7, 6, 8, 12, 9, 13, 3, 5, 13, 7, 7, 10, 11, 2, 12, 6, 6, 1, 5, 1, 15, 6, 12, 7, 11, 3, 7, 12, 13, 13, 13, 6, 14, 14, 4, 10, 8, 8, 8, 5, 8, 9, 12, 8, 14, 3, 8, 7, 3, 6, 14, 7, 3, 15, 11, 13, 6, 11, 3, 10, 6, 13, 12, 12, 10, 9, 5, 3, 8, 5, 4, 10, 11, 3, 15, 8, 11, 7, 6, 1, 3, 2, 11, 12, 15, 15, 15, 12, 13, 4, 2, 11, 12, 4, 11, 13, 10, 15, 3, 15, 15, 3, 7, 7, 3, 11, 15, 4, 7, 9, 10, 2, 9, 3, 14, 3, 13, 2, 5, 6, 15, 8, 12, 12, 10, 10, 3, 5, 5, 2, 2, 15, 15, 1, 14, 12, 8, 11, 5, 12, 11, 11, 5, 13, 2, 13, 14, 13, 9, 3, 14, 11, 15, 10, 10, 13, 13, 13, 8, 6, 14, 13, 9, 4, 9, 3, 13, 2, 1, 11, 2, 9, 9, 5, 3, 12, 14, 15, 3, 4, 10, 13, 15, 4, 2, 9, 15, 2, 3, 10, 3, 5, 11, 12, 5, 8, 4, 14, 6, 12, 4, 3, 9, 3, 2, 10, 5, 3, 3, 8, 15, 13, 8, 13, 7, 4, 9, 10, 4, 8, 1, 1, 14, 14, 2, 5, 4, 4, 13, 13, 10, 11, 15, 14, 5, 1, 7, 10, 7, 7, 15, 8, 3, 8, 7, 5, 11, 5, 11, 6, 5, 6, 13, 15, 5, 10, 7, 12, 12, 1, 9, 6, 11, 8, 7, 7, 9, 8, 3, 3, 12, 1, 14, 5, 1, 6, 14, 12, 6, 3, 9, 7, 3, 14, 4, 12, 4, 7, 7, 10, 9, 11, 6, 15, 9, 5, 1, 13, 13, 3, 2, 15, 11, 3, 1]

#testing: 0.10833333333333334 (percent of the time that number[n] == number[n-1]


Dualorder2= [1, 13, 5, 1, 5, 4, 1, 1, 8, 13, 7, 13, 5, 15, 4, 13, 10, 12, 5, 12, 2, 11, 15, 6, 1, 13, 8, 6, 4, 15, 12, 14, 7, 6, 14, 10, 13, 6, 8, 13, 15, 2, 5, 1, 9, 11, 1, 13, 1, 6, 12, 3, 11, 12, 10, 12, 15, 13, 10, 10, 3, 7, 14, 9, 12, 2, 4, 12, 15, 13, 11, 4, 10, 6, 13, 6, 8, 3, 2, 13, 14, 2, 9, 10, 3, 2, 13, 5, 7, 11, 6, 12, 8, 12, 7, 8, 11, 10, 15, 7, 14, 15, 12, 7, 4, 6, 3, 12, 15, 11, 2, 11, 13, 4, 15, 15, 12, 3, 9, 1, 6, 3, 10, 11, 8, 5, 9, 13, 13, 14, 15, 12, 15, 15, 8, 15, 3, 1, 1, 6, 13, 7, 1, 12, 1, 10, 4, 13, 4, 13, 15, 6, 5, 6, 8, 1, 7, 9, 7, 10, 12, 4, 6, 5, 9, 2, 12, 8, 15, 10, 9, 1, 8, 1, 14, 2, 4, 13, 2, 1, 8, 6, 15, 5, 8, 9, 8, 10, 11, 5, 15, 12, 10, 1, 5, 5, 3, 1, 9, 1, 10, 1, 12, 6, 2, 12, 3, 2, 3, 12, 2, 12, 14, 6, 6, 8, 12, 15, 7, 15, 8, 6, 14, 6, 13, 11, 5, 6, 5, 2, 10, 8, 10, 5, 10, 1, 9, 12, 13, 13, 1, 11, 5, 7, 8, 9, 5, 2, 8, 6, 14, 6, 14, 1, 11, 8, 3, 8, 6, 10, 12, 2, 14, 2, 3, 2, 3, 12, 1, 12, 7, 12, 11, 1, 14, 9, 7, 14, 1, 6, 15, 6, 9, 10, 10, 11, 12, 9, 14, 5, 3, 13, 9, 15, 11, 10, 13, 9, 15, 3, 4, 6, 8, 3, 9, 2, 15, 2, 6, 11, 4, 4, 15, 13, 8, 7, 14, 8, 3, 13, 9, 15, 12, 1, 13, 9, 13, 6, 15, 2, 4, 10, 3, 14, 8, 13, 10, 6, 15, 4, 14, 13, 12, 9, 7, 4, 4, 6, 4, 8, 15, 1, 10, 15, 9, 2, 1, 8, 2, 13]

# testing:c0.10833333333333334
#

#Dual Trainnig
training_total_runs = 6 #this is twice the number of trial n-back presentations







#Instruction Text
INSTRUCTIONTEXT= """INSTRUCTIONS: \n You will be presented with a series of lines drawn from two different categories. \n
Your mission, should you choose to accept it, is to figure out the categories- lines can be classified by pressing either 'k' or 'd' 
\n Be sure to be quick about it, or a time penalty will be enforced. \n There is also a secondary, concurrent task which the RA will explain.
N-BACK = """
