#!/usr/bin/python

#Load modules, these are the python modules that we need to run the game
import pygame, sys, os, math, time, datetime
from pygame.locals import *
from basic_cat_GameConstants import *
from basic_cat_GameWindow import *
import serial
import types
from cgkit.all import *
import cgkit.component as component
import cgkit.eventmanager as eventmanager
import cgkit.events as events
import cgkit.slots as slots
import cgkit.cgtypes as cgtypes
import cgkit._core
from numpy import *
import cgkit.flockofbirds as FOB
import random

#==== This is the main game class, where all the game pertinent stuff is initialized and the trial loop lives ====
class Game:
    def __init__(self):
         #initialize the pygame module
        pygame.mixer.init()
        pygame.init()
        
        #Create Window
        if FULL_SCREEN:
            self.screen = pygame.display.set_mode((0,0), FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(SCREEN_SIZE, NOFRAME) #This looks like full
    
        self.draw_rectlist = []
        self.erase_rectlist = []
    
        ScreenUpdate(self)  #updates the screen

        #This calls the function that prompts the user for the filename and trialset filename
        GameInputWindow(self,DATA_DIR,TRIALSET_DIR)   #returns trialset_fname and subject_fname
        
        
        #Load trialset and test how many trials
        trialset_file = open(TRIALSET_DIR+'/'+self.trialset_fname)
        trialset = trialset_file.readlines()
        trialset_file.close()
        self.trialset_len = len(trialset)-1
        self.max_score = self.trialset_len

        trialset_variables = trialset[0].replace('"','').split()
        for trial in trialset[1:]:
            values = trial.split()
            TRIAL_NUM.append(float(values[0]))
            CAT.append(float(values[1]))
            LENGTH.append(float(values[2]))
            THETA.append(float(values[3]))
            BETWEEN_BLOCKS.append(float(values[4]))

        #Abstracted file
        history = {
            'trial_num':[],
            'cat':[],
            'x':[],
            'y':[],
            'resp':[],
            'rt':[],
            }

        #Setup stuff
        self.trial_num = 0
        self.flag = 1
        self.total_score = 0
        self.current_score  = 0
        self.score_color = SCORE_COLOR
        self.score_position = (SCREEN_CENTER[0]-SCREEN_CENTER[0]/1.5,SCREEN_CENTER[1])
        self.exit = False
        
        #Timing
        clock = pygame.time.Clock()
        if os.name == 'nt': # are we running Windows?
            self.previous_time = time.clock()
        else:
            self.previous_time = time.time()

        self.state_time = 0
        self.rt = 0
        self.cat = 0
        self.x = 0
        self.y = 0
        self.resp = 0
        self.rt = 0
        
        #Trial Flags
        TRIAL_START = True       #Flag 1
        STIMULUS = False         #Flag 2
        FEEDBACK = False         #Flag 3
        ITI = False              #Flag 4
        TOO_SLOW = False         #Flag 5
        INVALID_KEY = False      #Flag 6

        #Initializing auditory feedback- loading sounds
        incorrectsound = pygame.mixer.Sound("C:\Users\Evan\Desktop\experiment_code\Soundeffects\FASTSAWING.wav")
        incorrectsound.set_volume(.3)
        correctsound =  pygame.mixer.Sound("C:\Users\Evan\Desktop\experiment_code\Soundeffects\HARP.wav")
        correctsound.set_volume(.3)
        invalidsound = pygame.mixer.Sound("C:\Users\Evan\Desktop\experiment_code\Soundeffects\FIREBIRDHIT.wav")
        invalidsound.set_volume(.6)
        slowsound = pygame.mixer.Sound("C:\Users\Evan\Desktop\experiment_code\Soundeffects\SLOWWW.wav")
        slowsound.set_volume(.3)
        
        #Game Pertinent Functions----------------------------------------------------------------------
        def CurrentEvent(self):
            if TRIAL_START:
                self.flag = 1
            if STIMULUS:
                self.flag = 2
            if FEEDBACK:
                self.flag = 3
            if ITI:
                self.flag = 4
            if TOO_SLOW:
                self.flag = 5
            if INVALID_KEY:
                self.flag = 6

        def BetweenBlocks(self):
            self.screen.fill(BACKGROUND_COLOR)
            font = pygame.font.Font(None, 36)
#            text = font.render("You collected "+ str(int(100*self.total_score/self.max_score))+ 
#                                "% of points available. Prepare for next round", 1, self.score_color)
            text = font.render("Good Job! Prepare for the next round", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, self.score_position))

        def GameHistoryUpdate(history):
            history_keys = [
                'trial_num',
                'cat',
                'x',
                'y',
                'resp',
                'rt',
                ]
            
            #Variables to save for output
            history['trial_num'].append(self.trial_num+1)
            history['cat'].append(self.cat)
            history['x'].append(self.x)
            history['y'].append(self.y)
            history['resp'].append(self.resp)
            history['rt'].append(self.rt)
            
            #Write the data (occurs after every trial
            WriteGameData(self,DATA_DIR,history,history_keys,) #This is a general function defined above
        #--------------------------------------------------------------------------------------------------------------        
        
        #iteration variables
        sample_time = 0
        trialnum = 0
        num_samples = 0
        x = 100
        y = 100
        trial_first_loop = True

        #This is the main trial loop---------------------------------------------------------------------------
        while trialnum < self.trialset_len:
            
            #Update Event Codes and timing
            #Set clock speed
            clock.tick(SAMPLING_RATE)
            if os.name == 'nt': # are we running Windows?
                self.current_time = time.clock()
            else:
                self.current_time = time.time()
            dt = self.current_time - self.previous_time
            self.previous_time += dt
            sample_time += dt
            num_samples += 1
        
            #Update trial flag
            CurrentEvent(self)
            
            if STIMULUS == False:
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.dict['key'] == K_ESCAPE:
                        self.exit = True
                        GameHistoryUpdate(history)   #This will call the saving function to save the game
                        pygame.display.quit()   #Closes the display
                        sys.exit()   #Calls interrupt to end game

            #Get current trialset variables on first run through the trial loop only
            if trial_first_loop:
                self.cat = CAT[trialnum]
                self.x = X[trialnum]
                self.y = Y[trialnum]
                self.between_blocks = BETWEEN_BLOCKS[trialnum]
                trial_first_loop = False
                    
            if TRIAL_START:
                #Update Event Codes and timing
                self.state_time += dt
                CurrentEvent(self)
                
                #Plot start                
                self.screen.fill(BACKGROUND_COLOR)
                font = pygame.font.Font(None, 72)
                text = font.render("+", 1, self.score_color)
                self.draw_rectlist.append(self.screen.blit(text, SCREEN_CENTER))
                
                if self.state_time > 1.0:
                    TRIAL_START = False
                    STIMULUS = True
                    FEEDBACK = False
                    ITI = False
                    TOO_SLOW = False
                    INVALID_KEY = False
                    self.state_time = 0
                
            if STIMULUS:
                #Update Event Codes and timing
                self.state_time += dt
                CurrentEvent(self)
                
                #Define line endpoints and draw the line
               # self.p1 = (SCREEN_CENTER[0]-100,SCREEN_CENTER[1]-100)
                #self.p2 = (SCREEN_CENTER[0]+100,SCREEN_CENTER[0]+100)
                #self.draw_rectlist.append(pygame.draw.lines(self.screen, (255,255,255), False, [self.p1,self.p2],2))


                #trig function- takes angle and length, returns

                #
                R = LENGTH/2
                X1 = R*cos(THETA)
                Y1 = R*sin(THETA)
                X2 = -X1
                Y2 = -Y1
                self.p1 = (SCREEN_CENTER[0]+X1,SCREEN_CENTER[1]+Y1)
                self.p2 = (SCREEN_CENTER[0]+X2,SCREEN_CENTER[1]+Y2)
                self.draw_rectlist.append(pygame.draw.lines(self.screen, (255,255,255), False, [self.p1,self.p2],2))



                
                #Get response
                for event_1 in pygame.event.get():
                    if event_1.type == KEYDOWN:
                        if event_1.dict['key'] == K_d:
                            self.resp = 1
                            self.rt = self.state_time
                    
                        elif event_1.dict['key'] == K_k:
                            self.resp = 2
                            self.rt = self.state_time
                            
                        elif event_1.dict['key'] == K_ESCAPE:
                            pygame.display.quit()   #Closes the display
                            sys.exit() #does not save halfway, however
                        else:
                            self.resp = -1
                            self.step_1_rt = self.state_time
                            INVALID_KEY = True
                            self.state_time = 0
                            break
                    
                        TRIAL_START = False
                        STIMULUS = False
                        FEEDBACK = True
                        ITI = False
                        TOO_SLOW = False
                        INVALID_KEY = False
                        self.state_time = 0
                
                #Enforce response deadline
                if self.state_time > 2.0:
                    TRIAL_START = False
                    STIMULUS = False
                    FEEDBACK = False
                    ITI = False
                    TOO_SLOW = True
                    INVALID_KEY = False
                    self.resp = -1
                    self.rt = -1
                    self.state_time = 0

            if FEEDBACK:
                #Update Event Codes and timing
                self.state_time += dt
                CurrentEvent(self)
                
                #Plot feedback
                self.screen.fill(BACKGROUND_COLOR)
                font = pygame.font.Font(None, 72)
                
                if self.cat == self.resp:
                    text = font.render("Correct", 1, self.score_color)
                    self.draw_rectlist.append(self.screen.blit(text, SCREEN_CENTER))
                    correctsound.set_volume(.3)
                    correctsound.play()
                else:
                    text = font.render("Incorrect", 1, self.score_color)
                    self.draw_rectlist.append(self.screen.blit(text, SCREEN_CENTER))
                    incorrectsound.set_volume(.3)
                    incorrectsound.play()
        
                if self.state_time > 1.75:
                    TRIAL_START = False
                    STIMULUS = False
                    FEEDBACK = False
                    ITI = True
                    TOO_SLOW = False
                    INVALID_KEY = False
                    self.state_time = 0
            
            if TOO_SLOW:
                #Update Event Codes and timing
                self.state_time += dt
                CurrentEvent(self)
                
                self.screen.fill(BACKGROUND_COLOR)
                font = pygame.font.Font(None, 72)
                text = font.render("TOO SLOW!", 1, self.score_color)
                self.draw_rectlist.append(self.screen.blit(text, SCREEN_CENTER))
                slowsound.play()
                if self.state_time > 1.5:
                    
                    #Update the game history right now
                    self.total_score += self.current_score
                    self.current_score = 0
                    
                    GameHistoryUpdate(history)
                    
                    #Reinitialize everything
                    trialnum += 1
                    self.trial_num = trialnum
                    num_samples = 0
                    trial_first_loop = True
                    
                    self.cat = 0
                    self.x = 0
                    self.y = 0
                    self.resp = 0
                    
                    TRIAL_START = True
                    STIMULUS = False
                    FEEDBACK = False
                    ITI = False
                    TOO_SLOW = False
                    INVALID_KEY = False
                    self.state_time = 0

            if INVALID_KEY:
                #Update Event Codes and timing
                self.state_time += dt
                CurrentEvent(self)
                
                self.screen.fill(BACKGROUND_COLOR)
                font = pygame.font.Font(None, 72)
                text = font.render("INVALID KEY!", 1, self.score_color)
                self.draw_rectlist.append(self.screen.blit(text, SCREEN_CENTER))
                invalidsound.set_volume(.3)
                invalidsound.play()
                
                if self.state_time > 1.5:
                    
                    #Update the game history right now
                    self.total_score += self.current_score
                    self.current_score = 0
                    
                    GameHistoryUpdate(history)
                    
                    #Reinitialize everything
                    trialnum += 1
                    self.trial_num = trialnum
                    num_samples = 0
                    trial_first_loop = True
                    
                    self.cat = 0
                    self.x = 0
                    self.y = 0
                    self.resp = 0
                    
                    TRIAL_START = True
                    STIMULUS = False
                    FEEDBACK = False
                    ITI = False
                    TOO_SLOW = False
                    INVALID_KEY = False
                    self.state_time = 0

            if ITI:
                #Update Event Codes and timing
                self.state_time += dt
                CurrentEvent(self)
                
                #Blank screen between trials
                self.screen.fill(BACKGROUND_COLOR)

                #Update all the variables
                if self.between_blocks == 1:
                    BetweenBlocks(self)
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            if self.state_time > 1.0:
                                #Update the game history right now
                                self.total_score += self.current_score
                                self.current_score = 0
                                
                                GameHistoryUpdate(history)
                                
                                #Reinitialize everything
                                trialnum += 1
                                self.trial_num = trialnum
                                num_samples = 0
                                trial_first_loop = True
                                
                                self.cat = 0
                                self.x = 0
                                self.y = 0
                                self.resp = 0
                                
                                TRIAL_START = True
                                STIMULUS = False
                                FEEDBACK = False
                                ITI = False
                                TOO_SLOW = False
                                INVALID_KEY = False
                                self.state_time = 0

                elif self.between_blocks == 0:

                    if self.state_time > 1.0:                    
                        #Update the game history right now
                        self.total_score += self.current_score
                        self.current_score = 0
                        
                        GameHistoryUpdate(history)
                        
                        #Reinitialize everything
                        trialnum += 1
                        self.trial_num = trialnum
                        num_samples = 0
                        trial_first_loop = True
                        
                        self.cat = 0
                        self.x = 0
                        self.y = 0
                        self.resp = 0
                        
                        TRIAL_START = True
                        STIMULUS = False
                        FEEDBACK = False
                        ITI = False
                        TOO_SLOW = False
                        INVALID_KEY = False
                        self.state_time = 0

            #Update screen
            ScreenUpdate(self)
            
if __name__ == '__main__': Game()




