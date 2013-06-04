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



Dualorder=[12, 13, 1, 8, 1, 13, 13, 15, 3, 8, 8, 9, 11, 5, 6, 15, 3, 7, 13, 13, 3, 14, 7, 5, 6, 1, 1, 14, 7, 9, 9, 11, 2, 10, 5, 8, 10, 9, 12, 6, 15, 2, 7, 1, 10, 11, 8, 15, 14, 6, 7, 11, 1, 6, 15, 5, 11, 13, 10, 12, 4, 2, 1, 12, 9, 11, 14, 11, 11, 7, 12, 12, 14, 3, 1, 8, 13, 12, 15, 9, 14, 10, 7, 6, 5, 2, 13, 10, 8, 12, 3, 4, 2, 2, 1, 6, 9, 15, 11, 12, 4, 11, 15, 2, 9, 4, 8, 12, 10, 12, 9, 1, 4, 13, 3, 15, 3, 14, 4, 2, 2, 3, 9, 10, 3, 14, 15, 8, 4, 7, 5, 15, 5, 15, 14, 10, 4, 3, 5, 5, 4, 6, 13, 14, 7, 8, 2, 10, 7, 3, 5, 6, 1, 6, 11, 8, 5, 10, 14, 1, 3, 4, 2, 12, 5, 11, 7, 14, 9, 9, 6, 13, 7, 8, 6, 4, 2, 13, 10, 4, 12, 13, 1, 8, 1, 13, 13, 15, 3, 8, 8, 9, 11, 5, 6, 15, 3, 7, 13, 13, 3, 14, 7, 5, 6, 1, 1, 14, 7, 9, 9, 11, 2, 10, 5, 8, 10, 9, 12, 6, 15, 2, 7, 1, 10, 11, 8, 15, 14, 6, 7, 11, 1, 6, 15, 5, 11, 13, 10, 12, 4, 2, 1, 12, 9, 11, 14, 11, 11, 7, 12, 12, 14, 3, 1, 8, 13, 12, 15, 9, 14, 10, 7, 6, 5, 2, 13, 10, 8, 12, 3, 4, 2, 2, 1, 6, 9, 15, 11, 12, 4, 11, 15, 2, 9, 4, 8, 12, 10, 12, 9, 1, 4, 13, 3, 15, 3, 14, 4, 2, 2, 3, 9, 10, 3, 14, 15, 8, 4, 7, 5, 15, 5, 15, 14, 10, 4, 3, 5, 5, 4, 6, 13, 14, 7, 8, 2, 10, 7, 3, 5, 6, 1, 6, 11, 8, 5, 10, 14, 1, 3, 4, 2, 12, 5, 11, 7, 14, 9, 9, 6, 13, 7, 8, 6, 4, 2, 13, 10, 4]


#Dual Trainnig
training_total_runs = 6 #this is twice the number of trial n-back presentations







#Instruction Text
INSTRUCTIONTEXT= """INSTRUCTIONS: \n You will be presented with a series of  images drawn from two different categories. \n

Your task, should you choose to accept, is to answer the Very Important Question: \n\n Who's on First??

N-BACK = """
