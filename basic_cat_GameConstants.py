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

#Instruction Text

INSTRUCTIONTEXT= """INSTRUCTIONS: \n You will be presented with a series of  images drawn from two different categories. \n

Your task, should you choose to accept, is to answer the Very Important Question: \n\n Who's on First??

N-BACK = """
