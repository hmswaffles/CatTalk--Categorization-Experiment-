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
        
        pygame.init()
        pygame.mixer.init()
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
       # print LENGTH

        #Abstracted file
        history = {
            'trial_num':[],
            'cat':[],
            'length':[],
            'theta':[],
            'resp':[],
            'rt':[],
            'DTcorrect':[],
            'DTrt':[]
            }

        #Setup stuff
        font = pygame.font.Font('C:\\Windows\\Fonts\\georgia.ttf', 48)
        
        self.trial_num = 0
        self.flag = 1
        self.total_score = 0
        self.current_score  = 0
        self.score_color = SCORE_COLOR
        self.score_position = (SCREEN_CENTER[0]-SCREEN_CENTER[0]/1.5,SCREEN_CENTER[1])
        self.exit = False
        self.Dual_Counter = 0
        self.DUAL_COUNT = 0
        self.image =[]
        
        #Timing
        clock = pygame.time.Clock()
        if os.name == 'nt': # are we running Windows?
            self.previous_time = time.clock()
        else:
            self.previous_time = time.time()

        self.state_time = 0
        self.rt = 0
        self.cat = 0
        self.length = 0
        self.theta = 0
        self.resp = 0
        self.rt = 0
        self.DTcorrect = 0
        self.DTrt = 0
        
        #Trial Flags
        TRIAL_START = False       #Flag 1
        STIMULUS = False         #Flag 2
        FEEDBACK = False         #Flag 3
        ITI = False              #Flag 4
        TOO_SLOW = False         #Flag 5
        INVALID_KEY = False      #Flag 6    
        DUAL_TASK_P = False        #Flag 7 P-present
        DUAL_TASK_R =False       #Flag 8 R-record
        DUAL_TRAINING_T= False
        DUAL_TRAINING_1 = False
        DUAL_TRAINING_R = False
        DUAL_TRAINING_N = False
        DUAL_TRAINING_END = False


        #Initializing auditory feedback- loading sounds
        incorrectsound = pygame.mixer.Sound("C:\Users\Evan\Desktop\experiment_code\Soundeffects\FASTSAWING.wav")
        incorrectsound.set_volume(.3)
        correctsound =  pygame.mixer.Sound("C:\Users\Evan\Desktop\experiment_code\Soundeffects\HARP.wav")
        correctsound.set_volume(.3)
        invalidsound = pygame.mixer.Sound("C:\Users\Evan\Desktop\experiment_code\Soundeffects\FIREBIRDHIT.wav")
        invalidsound.set_volume(.6)
        slowsound = pygame.mixer.Sound("C:\Users\Evan\Desktop\experiment_code\Soundeffects\SLOWWW.wav")
        slowsound.set_volume(.2)

        #Loading dual task imagesprint 'loading images'
        DT0= pygame.image.load("C:\\Users\\Evan\\Desktop\\experiment_code\\Dual\\0.png")
        DT1= pygame.image.load("C:\\Users\Evan\\Desktop\\experiment_code\\Dual\\1.png")
        DT2= pygame.image.load("C:\\Users\Evan\\Desktop\\experiment_code\\Dual\\2.png")
        DT3= pygame.image.load("C:\\Users\Evan\\Desktop\\experiment_code\\Dual\\3.png")
        DT4= pygame.image.load("C:\\Users\Evan\\Desktop\\experiment_code\\Dual\\4.png")
        DT5= pygame.image.load("C:\\Users\Evan\\Desktop\\experiment_code\\Dual\\5.png")
        DT6= pygame.image.load("C:\\Users\Evan\\Desktop\\experiment_code\\Dual\\6.png")
        DT7= pygame.image.load("C:\\Users\Evan\\Desktop\\experiment_code\\Dual\\7.png")
       
        DT8= pygame.image.load("C:\\Users\\Evan\\Desktop\\experiment_code\\Dual\\8.png")
        DT9= pygame.image.load("C:\\Users\\Evan\\Desktop\\experiment_code\\Dual\\9.png")
        DT10= pygame.image.load("C:\\Users\\Evan\\Desktop\\experiment_code\\Dual\\10.png")
        DT11= pygame.image.load("C:\\Users\\Evan\\Desktop\\experiment_code\\Dual\\11.png")
        DT12= pygame.image.load("C:\\Users\\Evan\\Desktop\\experiment_code\\Dual\\12.png")
        DT13= pygame.image.load("C:\\Users\\Evan\\Desktop\\experiment_code\\Dual\\13.png")
        DT14= pygame.image.load("C:\\Users\\Evan\\Desktop\\experiment_code\\Dual\\14.png")
        #DT15= pygame.image.load("C:\\Users\\Evan\\Desktop\\experiment_code\\Dual\\15.png")
        DUALRECT = DT0.get_rect()
        dual_ls_image = [DT0,DT1,DT2,DT3,DT4,DT5,DT6,DT7,DT8,DT9,DT10,DT11,DT12,DT13,DT14,]
      
        if self.N ==1:
            Dualorder = Dualorder1
        elif self.N ==2:
            Dualorder = Dualorder2
        else:
            print'please generate a dualorder list, save it as Dualordern in basic_cat_game_constants'," then edit line ~160 in basic_cat_exp"
            pygame.display.quit()   #Closes the display
            sys.exit()
            
        #dual text- renders here as to avoid flickering whilst in-loop
            #dual task
        Adual="Was the previous image the same as the one " + ' ' + str(self.N)+ ' '+ "presentation(s) ago? \n Spacebar= Yes, Enter =No"
        Amy_rectt = pygame.Rect(((SCREEN_CENTER[0]-250,SCREEN_CENTER[1]-250),(SCREEN_CENTER[0]+250,SCREEN_CENTER[1]+250)))
        ADualtext = render_textrect(Adual, font, Amy_rectt, (0,0,0), (120,120,120),1)

            #dual training:
        dualtext="DUAL TASK TRAINING. \n This will run" +' '+ str(training_total_runs/2) +' ' + " times, after which you will start the experiment proper. \n Please remember the grid " +' '+ str(self.N)+' ' +  "presentation(s) back "
        my_rectt = pygame.Rect((40, 40, 600, 600))
        text_t = render_textrect(dualtext, font, my_rectt, (0,0,0), (120,120,120),1)        
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
            if DUAL_TASK_P:
                self.flag = 7
            if DUAL_TASK_R:
                self.flag = 8
            if DUAL_TRAINING_T:
                self.flag =9
            if DUAL_TRAINING_1:
                self.flag =10
            if DUAL_TRAINING_N:
                self.flag = 11
            if DUAL_TRAINING_R:
                self.flag = 12
            if DUAL_TRAINING_END:
                self.flag = 13
                
        
                

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
                'length',
                'theta',
                'resp',
                'rt',
                'DTcorrect',
                'DTrt',
                ]
            
            #Variables to save for output
            history['trial_num'].append(self.trial_num+1)
            history['cat'].append(self.cat)
            history['length'].append(self.length)
            history['theta'].append(self.theta)
            history['resp'].append(self.resp)
            history['rt'].append(self.rt)
            history['DTcorrect'].append(self.DTcorrect)
            history['DTrt'].append(self.DTrt)
            
            #Write the data (occurs after every trial
            WriteGameData(self,DATA_DIR,history,history_keys,) #This is a general function defined in basiccatgamewindow
        #--------------------------------------------------------------------------------------------------------------
  
        
        #iteration variables
        sample_time = 0
        trialnum = 0
        num_samples = 0
        x = 100
        y = 100
        trial_first_loop = True
        training = True

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
         ###               
            if trial_first_loop and training: #if absolute first time, throws to training
                self.cat = CAT[trialnum]
                self.length = LENGTH[trialnum]
                self.theta = THETA[trialnum]
                self.between_blocks = BETWEEN_BLOCKS[trialnum]
                #DUAL_COUNTER=0
                #Dual_count=0
                TRIAL_START = False
                STIMULUS = False
                FEEDBACK = False
                ITI = False
                TOO_SLOW = False
                INVALID_KEY = False
                DUAL_TASK_P = False
                DUAL_TASK_R =False
                DUAL_TRAINING_T= True
                DUAL_TRAINING_1 = False
                DUAL_TRAINING_R = False
                DUAL_TRAINING_N = False
                DUAL_TRAINING_END = False
                trial_first_loop = False
                training = False
                self.state_time = 0
                
            if trial_first_loop and not training:
                self.cat = CAT[trialnum]
                self.length = LENGTH[trialnum]
                self.theta = THETA[trialnum]
                self.between_blocks = BETWEEN_BLOCKS[trialnum]
                #DUAL_COUNTER=0
                #Dual_count=0


                
                TRIAL_START = True
                STIMULUS = False
                FEEDBACK = False
                ITI = False
                TOO_SLOW = False
                INVALID_KEY = False
                DUAL_TASK_P = False
                DUAL_TASK_R =False
                DUAL_TRAINING_T= False
                DUAL_TRAINING_1 = False
                DUAL_TRAINING_R = False
                DUAL_TRAINING_N = False
                DUAL_TRAINING_END = False
                trial_first_loop = False
                training = False
                self.state_time = 0


                    
            if TRIAL_START:
                #Update Event Codes and timing
                self.state_time += dt
                CurrentEvent(self)
                
                #Plot start                
                self.screen.fill(BACKGROUND_COLOR)
                #font = pygame.font.Font(None, 72) font is georgia, already above
                text = font.render("+", 1, self.score_color)
               #### self.draw_rectlist.append(self.screen.blit(text, SCREEN_CENTER))
                self.screen.blit(text, (SCREEN_CENTER[0]-15,SCREEN_CENTER[1]-15))
                pygame.display.flip()
                if self.state_time > FIXATION_TIME:
                    TRIAL_START = False
                    STIMULUS = True
                    FEEDBACK = False
                    ITI = False
                    TOO_SLOW = False
                    INVALID_KEY = False
                    DUAL_TASK_P = False
                    DUAL_TASK_R =False
                    DUAL_TRAINING_T= False
                    DUAL_TRAINING_1 = False
                    DUAL_TRAINING_R = False
                    DUAL_TRAINING_N = False
                    DUAL_TRAINING_END = False
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

                #draws the lines:
               
                R = float(LENGTH[(trialnum)])/2
                X1 = R*cos(THETA[(trialnum)])
                Y1 = R*sin(THETA[(trialnum)])
               # X2 = -X1
               # Y2 = -Y1
                self.p1 = (SCREEN_CENTER[0]+X1,SCREEN_CENTER[1]+Y1)
                self.p2 = (SCREEN_CENTER[0]-X1,SCREEN_CENTER[1]-Y1)

                self.screen.fill(BACKGROUND_COLOR)
                #self.draw_rectlist.append(pygame.draw.aaline(self.screen, (255,255,255), self.p1,self.p2,2))
                pygame.draw.aaline(self.screen, (0,0,0), self.p1,self.p2,2)
                pygame.display.flip()


                
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
                            
                          


                            TRIAL_START = False
                            STIMULUS = False
                            FEEDBACK = False
                            ITI = False
                            TOO_SLOW = False
                            INVALID_KEY = True
                            invalidsoundflag = True
                            DUAL_TASK_P= False
                            DUAL_TASK_R=False
                            DUAL_TRAINING_T= False
                            DUAL_TRAINING_1 = False
                            DUAL_TRAINING_R = False
                            DUAL_TRAINING_N = False
                            DUAL_TRAINING_END = False
                            self.state_time = 0
                            break
                    
                        TRIAL_START = False
                        STIMULUS = False
                        FEEDBACK = True
                        correctsoundflag=True #insures that the sound is only initalized once.
                        incorrectsoundflag=True ### this choice is made below, but because of the while loop, both have to be set here
                        ITI = False
                        TOO_SLOW = False
                        INVALID_KEY = False
                        DUAL_TASK_P= False
                        DUAL_TASK_R=False
                        DUAL_TRAINING_T= False
                        DUAL_TRAINING_1 = False
                        DUAL_TRAINING_R = False
                        DUAL_TRAINING_N = False
                        DUAL_TRAINING_END = False
                        self.state_time = 0
                
                #Enforce response deadline
                if self.state_time > 2.0:
                    TRIAL_START = False
                    STIMULUS = False
                    FEEDBACK = False
                    ITI = False
                    TOO_SLOW = True
                    slowsoundflag = True
                    INVALID_KEY = False
                    DUAL_TASK_P = False
                    DUAL_TASK_R = False
                    DUAL_TRAINING_T= False
                    DUAL_TRAINING_1 = False
                    DUAL_TRAINING_R = False
                    DUAL_TRAINING_N = False
                    DUAL_TRAINING_END = False
                    self.resp = -1
                    self.rt = -1
                    self.state_time = 0

            if FEEDBACK:
                #Update Event Codes and timing
                self.state_time += dt
                CurrentEvent(self)
                
                #Plot feedback
                self.screen.fill(BACKGROUND_COLOR)
                #font = pygame.font.Font(None, 72) again, font is already rendered above
                
                if self.cat == self.resp:
                    text = font.render("Correct", 1, self.score_color)
                    #self.draw_rectlist.append(self.screen.blit(text, (SCREEN_CENTER[0]-50,SCREEN_CENTER[1]))
                    self.screen.blit(text, (SCREEN_CENTER[0]-80,SCREEN_CENTER[1]-30))
                    pygame.display.flip()
                    if correctsoundflag:
                        correctsound.set_volume(.3)
                        correctsound.play()
                    correctsoundflag=False
                else:
                    text = font.render("Incorrect", 1, self.score_color)
                    #self.draw_rectlist.append(self.screen.blit(text, SCREEN_CENTER))
                    self.screen.blit(text, (SCREEN_CENTER[0]-80,SCREEN_CENTER[1]-30))
                    pygame.display.flip()
                    if incorrectsoundflag:
                        incorrectsound.set_volume(.3)
                        incorrectsound.play()
                    incorrectsoundflag=False
        
                if self.state_time > 1.75:
                    pygame.mixer.stop()
                    TRIAL_START = False
                    STIMULUS = False
                    FEEDBACK = False
                    ITI = False
                    TOO_SLOW = False
                    INVALID_KEY = False
                    DUAL_TASK_P= True
                    DUAL_TASK_R = False
                    #DUALFLAG = True
                    DUAL_TRAINING_T= False
                    DUAL_TRAINING_1 = False
                    DUAL_TRAINING_R = False
                    DUAL_TRAINING_N = False
                    DUAL_TRAINING_END = False
                    self.state_time = 0
            
            if TOO_SLOW:
                #Update Event Codes and timing
                self.state_time += dt
                CurrentEvent(self)
                
                self.screen.fill(BACKGROUND_COLOR)
                #font = pygame.font.Font(None, 72)font isinitialized above
                text = font.render("TOO SLOW!", 1, self.score_color)
                self.screen.blit(text, (SCREEN_CENTER[0]-50,SCREEN_CENTER[1]))
                pygame.display.flip()
                if slowsoundflag:
                    slowsound.play()
                slowsoundflag=False
                if self.state_time > 1.9:
                    
                    #Update the game history right now
                    self.total_score += self.current_score
                    self.current_score = 0
                    
                    GameHistoryUpdate(history)
                    
                    #Reinitialize everything
                    trialnum += 1
                    self.trial_num = trialnum
                    num_samples = 0
                    trial_first_loop = False
                    
                    #self.cat = 0
                    #self.x = 0
                    #self.y = 0
                    self.resp = 0

                    pygame.mixer.stop()
                    TRIAL_START = False
                    STIMULUS = False
                    FEEDBACK = False
                    ITI = False
                    TOO_SLOW = False
                    INVALID_KEY = False
                    DUAL_TASK_P = True
                    DUAL_TASK_R=False
                    DUAL_TRAINING_T= False
                    DUAL_TRAINING_1 = False
                    DUAL_TRAINING_R = False
                    DUAL_TRAINING_N = False
                    DUAL_TRAINING_END = False
                    
                    self.state_time = 0

            if INVALID_KEY:
                #Update Event Codes and timing
                self.state_time += dt
                #CurrentEvent(self)
                self.screen.fill(BACKGROUND_COLOR)
               
                #font = pygame.font.Font(None, 72)
                text = font.render("INVALID KEY", 1, self.score_color)
                #self.draw_rectlist.append(self.screen.blit(text, SCREEN_CENTER))
                self.screen.blit(text, (SCREEN_CENTER[0]-120,SCREEN_CENTER[1]-50))
                pygame.display.flip()
                
              
               
                if invalidsoundflag:
                    invalidsound.set_volume(.3)
                    invalidsound.play()
                    invalidsoundflag = False
                if self.state_time > 1.5:
                    
                    #Update the game history right now
                    self.total_score += self.current_score
                    self.current_score = 0
                    
                    GameHistoryUpdate(history)
                    
                    #Reinitialize everything
                    trialnum += 1
                    self.trial_num = trialnum
                    num_samples = 0
                    trial_first_loop = False
                    
                    #self.cat = 0
                    #self.length = 0
                    #self.theta = 0
                    self.resp = -2

                    pygame.mixer.stop()
                    TRIAL_START = False
                    STIMULUS = False
                    FEEDBACK = False
                    ITI = False
                    TOO_SLOW = False
                    INVALID_KEY = False
                    DUAL_TASK_P= True
                    DUAL_TASK_R = False
                    DUAL_TRAINING_T= False
                    DUAL_TRAINING_1 = False
                    DUAL_TRAINING_R = False
                    DUAL_TRAINING_N = False
                    DUAL_TRAINING_END = False
                    invalidsoundflag = False
                    self.state_time = 0


                    

            if DUAL_TASK_P:
                #to do
                #potentially need to reset self.statetime to get a raw RT for dual task?
                #present in the n=1 back and the n=2 back, with a 10% possibility of repition
                #use spacebar
                #print self.DUAL_COUNT, self.Dual_Counter, 'n',self.N
                self.state_time += dt
                CurrentEvent(self)
                
                self.screen.fill(BACKGROUND_COLOR)
                image=dual_ls_image[Dualorder[self.Dual_Counter]]       
                self.screen.blit(dual_ls_image[Dualorder[self.Dual_Counter]], (SCREEN_CENTER[0]-150,SCREEN_CENTER[1]-150))
                pygame.display.flip()
              
                if self.state_time > DUAL_DISP_TIME:        
                    if self.DUAL_COUNT<self.N:
                        #just display, if before the right amount of n
                        self.Dual_Counter += 1
                        self.DUAL_COUNT += 1
                        self.screen.fill(BACKGROUND_COLOR)
                        TRIAL_START = False
                        STIMULUS = False
                        FEEDBACK = False
                        ITI = True
                        TOO_SLOW = False
                        INVALID_KEY = False
                        DUAL_TASK_P = False
                        DUAL_TASK_R = False
                        DUAL_TRAINING_T= False
                        DUAL_TRAINING_1 = False
                        DUAL_TRAINING_R = False
                        DUAL_TRAINING_N = False
                        DUAL_TRAINING_END = False
                        self.state_time = 0
                    
                      
                    else:#record response before moving on
                        #print 'jjjjjjjjjjjjjjjj'
                        self.screen.fill(BACKGROUND_COLOR)
                        TRIAL_START = False
                        STIMULUS = False
                        FEEDBACK = False
                        ITI = False
                        TOO_SLOW = False
                        INVALID_KEY = False
                        DUAL_TASK_P = False
                        DUAL_TRAINING_T= False
                        DUAL_TRAINING_1 = False
                        DUAL_TRAINING_R = False
                        DUAL_TRAINING_N = False
                        DUAL_TRAINING_END = False
               
                        
                        if Dualorder[DUALCOUNTER] == Dualorder[DUALCOUNTER-self.N]:
                            correctresponse= 'space'
                        else:
                            correctresponse= 'return'
                            
                        DUAL_TASK_R = True
                        self.state_time = 0
                        #self.Dual_Counter += 1--- this is incremented under DUAL_TASK_R. Don't ask me why I did that, I have no idea.
                        self.DUAL_COUNT += 1
                

                


                    
            if DUAL_TASK_R:
                
                
                self.state_time += dt
                CurrentEvent(self)
                #instruct and record
                #display instruction
                #oold dual task, paste here from bottom
                self.screen.fill(BACKGROUND_COLOR)  
                self.screen.blit(ADualtext, (SCREEN_CENTER[0]-350,SCREEN_CENTER[1]-250))
                #print 'dualRR'
                pygame.display.flip()
                time.sleep(1)#################################################
                
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        
                        if event.dict['key'] == K_RETURN:
                            if 'return'==correctresponse:
                                self.DTcorrect=1
                                self.DTrt = self.state_time
                                ITI=True
                                DUAL_TASK_R=False
                                self.Dual_Counter += 1
                                self.state_time =0
                                
                            else:
                                self.DTcorrect=0
                                self.DTrt = self.state_time
                                ITI=True
                                DUAL_TASK_R=False
                                self.Dual_Counter += 1
                                self.state_time =0
                                
                        elif event.dict['key'] == K_SPACE:
                            if 'space'==correctresponse:
                                self.DTcorrect=1
                                self.DTrt = self.state_time
                                ITI=True
                                DUAL_TASK_R=False
                                self.Dual_Counter += 1
                                self.state_time =0
                                
                            else:
                                self.DTcorrect=0
                                self.DTrt = self.state_time
                                ITI=True
                                DUAL_TASK_R=False
                                self.Dual_Counter += 1
                                self.state_time =0
                                
                        elif event.dict['key'] == K_ESCAPE:
                            pygame.display.quit()   #Closes the display
                            sys.exit() #does not save halfway, however. DONT PRESS ESCAPE!
                            break
                          
        
                    
                if self.state_time > 3.0:

                    
                    TRIAL_START = False
                    STIMULUS = False
                    FEEDBACK = False
                    ITI = True
                    TOO_SLOW = False
                    INVALID_KEY = False
                    DUAL_TASK_P = False
                    DUAL_TASK_R = False
                    DUAL_TRAINING_T= False
                    DUAL_TRAINING_1 = False
                    DUAL_TRAINING_N= False
                    DUAL_TRAINING_R = False
                    DUAL_TRAINING_END = False
                    self.DTcorrect = -1
                    self.DUAL_COUNT += 1
                    self.Dual_Counter +=1
                    self.state_time =0

                    
##                        else:
##                            TRIAL_START = False
##                            STIMULUS = False
##                            FEEDBACK = False
##                            ITI = False
##                            TOO_SLOW = False
##                            INVALID_KEY = False
##                            DUAL_TASK_P = False
##                            DUAL_TASK_R = True
##                            #DUALFLAG = True
                            
                            
                                 
               
                
               

            if DUAL_TRAINING_T:
                
                self.state_time += dt
                CurrentEvent(self)
                
                #display "welcome, fellow potentially nondescript RPP person. hereabouts begins your training on the distractor task. 
                #this will run five times, before a splash screen, after which you will start the experiment proper"
                #you are going to have to remember sequences of randomly generated white-on-black grids, n presentations ago
                #sleep or press enter and escape



     
                
                self.draw_rectlist.append(self.screen.blit(text_t, (SCREEN_CENTER[0]-300,SCREEN_CENTER[1]-200)))


                pygame.display.update()
                time.sleep(.5)

                
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.dict['key'] == K_RETURN:
                            
                            self.state_time = 0
                            #where to go next-> training_1
                            self.screen.fill(BACKGROUND_COLOR)
                            TRIAL_START = False
                            STIMULUS = False
                            FEEDBACK = False
                            ITI = False
                            TOO_SLOW = False
                            INVALID_KEY = False
                            DUAL_TASK_P = False
                            DUAL_TASK_R = False
                            DUAL_TRAINING_T = False
                            DUAL_TRAINING_1= True
                            DUAL_TRAINING_N = False
                            DUAL_TRAINING_R= False
                            DUAL_TRAINING_END = False
                            #print 'only seeing this once ', self.DUAL_COUNT, self.Dual_Counter
                            #DUAL_COUNT is the nth training run, self.Dual_counter controls which grid to show.
                            
                        elif event.key == K_ESCAPE:
                            pygame.display.quit()   #Closes the display
                            sys.exit()

                            
                        else:
                            DUAL_TRAINING =True
                


             
                   
                            
                
            if DUAL_TRAINING_1: #first n times through Dual Training
                    self.state_time += dt
                    CurrentEvent(self)


    
                    self.screen.blit(dual_ls_image[Dualorder[self.Dual_Counter]], (SCREEN_CENTER[0]-150,SCREEN_CENTER[1]-150))
                    pygame.display.update()
                    time.sleep(.5)

                    
                    if self.state_time > DUAL_DISP_TIME:
                        
                        self.Dual_Counter +=1
                        self.DUAL_COUNT +=1
                        TRIAL_START = False
                        STIMULUS = False
                        FEEDBACK = False
                        ITI = False
                        TOO_SLOW = False
                        INVALID_KEY = False
                        DUAL_TASK_P = False
                        DUAL_TASK_R = False
                        DUAL_TRAINING_T = False
                        DUAL_TRAINING_END = False
                        DUAL_TRAINING_N = False
                        
                        self.state_time=0

                        

             
                        if self.DUAL_COUNT < self.N+1:
                            
                            DUAL_TRAINING_N = False
                            DUAL_TRAINING_1 = True
                            
                            
                        else:
                            DUAL_TRAINING_N = False
                            DUAL_TRAINING_1 =False
                            DUAL_TRAINING_R = True
                            
                            



                
              
                   
            if DUAL_TRAINING_N:
                    
                   # print 'top of training_N'
                    self.state_time += dt
                    CurrentEvent(self)
                   # self.screen.fill(BACKGROUND_COLOR)
                   # ScreenUpdate(self)
                    #print Dualorder[self.Dual_Counter]
                 
                    #self.screen.blit(dual_ls_image[Dualorder[self.Dual_Counter]] , DUALRECT)
                    self.screen.blit(dual_ls_image[Dualorder[self.Dual_Counter]], (SCREEN_CENTER[0]-150,SCREEN_CENTER[1]-150))
                    pygame.display.update()
                    time.sleep(.5)
                    if self.state_time > DUAL_DISP_TIME:
                        # self.screen.fill(BACKGROUND_COLOR)
                        #ScreenUpdate(self)
                        
                        
                        TRIAL_START = False
                        STIMULUS = False
                        FEEDBACK = False
                        ITI = False
                        TOO_SLOW = False
                        INVALID_KEY = False
                        DUAL_TASK_P = False
                        DUAL_TASK_R = False
                        DUAL_TRAINING_T= False
                        DUAL_TRAINING_1 = False
                        DUAL_TRAINING_R = True
                        DUAL_TRAINING_END =False
                        DUAL_TRAINING_N = False

                        self.Dual_Counter +=1
                        self.DUAL_COUNT +=1
                        self.state_time = 0
                        
                        #self.state_time=0 the instructions should cancel out in in-person data analysis...
                    
                             




                    
            if DUAL_TRAINING_R:
                self.state_time += dt
                CurrentEvent(self)
                self.screen.fill(BACKGROUND_COLOR) 
                dualtext="Was that grid image the same as the one "  + str(self.N) + " presentation(s) ago? \n Spacebar= Yes, Enter =No"
                my_rectt = pygame.Rect((40, 40, 500, 500))
                text = render_textrect(dualtext, font, my_rectt, (0,0,0), (120,120,120))
                self.draw_rectlist.append(self.screen.blit(text, (SCREEN_CENTER[0]-250,SCREEN_CENTER[1]-250)))
                pygame.display.update()
                
                if Dualorder[self.Dual_Counter] == Dualorder[self.Dual_Counter-self.N]:
                    correctresponse= 'space'
                else:
                    correctresponse= 'return'               
               # print 'TRAINING_R: ', self.DUAL_COUNT, training_total_runs,'n',self.N
                #self.DUAL_COUNT >= training_total_runs
                #time.sleep(.1)
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        self.state_time=0
                        self.Dual_Counter += 1
                        self.DUAL_COUNT +=1
                        if event.dict['key'] == K_RETURN:
                            if 'return'==correctresponse:
                                self.DTcorrect=1
                            else:
                                self.DTcorrect=0
                            self.DTrt = self.state_time                        
                            self.screen.fill(BACKGROUND_COLOR)
                            pygame.display.update()
                            
                            if self.DUAL_COUNT > training_total_runs:
                                DUAL_TRAINING_R = False
                                DUAL_TRAINING_N = False
                                DUAL_TRAINING_T = False
                                DUAL_TRAINING_1 = False
                                DUAL_TRAINING_END = True
                                #record,
                                self.state_time=0
                            elif self.DUAL_COUNT < self.N+1:
                                DUAL_TRAINING_R = False
                                DUAL_TRAINING_1 = True
                                self.state_time = 0
                            else:
                                DUAL_TRAINING_R = False
                                DUAL_TRAINING_N = True
                                self.state_time=0
                                
                        elif event.dict['key'] == K_SPACE:
                            if 'space'==correctresponse:
                                self.DTcorrect=1
                            else:
                                self.DTcorrect=0                                
                            self.DTrt = self.state_time                           
                            self.screen.fill(BACKGROUND_COLOR)
                            pygame.display.update()

                          
                            if self.DUAL_COUNT > training_total_runs:
                                DUAL_TRAINING_R = False
                                DUAL_TRAINING_N = False
                                DUAL_TRAINING_T = False
                                DUAL_TRAINING_1 = False
                                DUAL_TRAINING_END = True
                            elif self.DUAL_COUNT < self.N+1:
                                DUAL_TRAINING_R = False
                                DUAL_TRAINING_1 = True
                                self.state_time=0
                              #  print 'gutbye;'
                            else:
                                DUAL_TRAINING_R = False
                                DUAL_TRAINING_N = True
                                self.state_time=0
                               # print 'challo'

                            
                                
                        elif event.dict['key'] == K_ESCAPE:
                            pygame.display.quit()   #Closes the display
                            sys.exit() #does not save halfway, however. DONT PRESS ESCAPE!
                            break

                            
                    if self.state_time > 2.5:
                       # print 'meep'
                        TRIAL_START = False
                        STIMULUS = False
                        FEEDBACK = False
                        ITI = False
                        TOO_SLOW = False
                        INVALID_KEY = False
                        DUAL_TASK_P = False
                        DUAL_TASK_R = False
                        DUAL_TRAINING_T= False
                        self.state_time=0

                        if self.DUAL_COUNT > training_total_runs:
                            DUAL_TRAINING_R = False
                            DUAL_TRAINING_END = True
                        elif self.DUAL_COUNT < self.N+1:
                            DUAL_TRAINING_R = False
                            DUAL_TRAINING_1 = True
                            self.state_time=0
                        else:
                            DUAL_TRAINING_R = False
                            DUAL_TRAINING_N = True
                            self.state_time=0
                            
                    
                   
                        


                        
                              
            if DUAL_TRAINING_END:
                #print 'end'
                textt = "The training is now over, press RETURN to start the experiment. Please categorize the lines with either 'k' or 'd'"
                rect = pygame.Rect((100,100,400,400))
                etext = render_textrect(textt,font,rect,(0,0,0), (120,120,120))
                self.draw_rectlist.append(self.screen.blit(etext, (SCREEN_CENTER[0]-200,SCREEN_CENTER[1]-200)))
                pygame.display.update()
                #time.sleep(.1)
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.dict['key'] == K_RETURN:
                            FEEDBACK = False
                            ITI = False
                            TOO_SLOW = False
                            INVALID_KEY = False
                            DUAL_TASK_P = False
                            DUAL_TASK_R = False
                            DUAL_TRAINING_T = False
                            DUAL_TRAINING_1= False
                            DUAL_TRAINING_R= False
                            DUAL_TRAINING_N = False
                            DUAL_TRAINING_END = False
                            TRIAL_START = False
                            trial_first_loop = True
                            training = False
                            self.DUAL_COUNT = 0
                            self.state_time=0
                     
                      
                


           
            if ITI:
                #Update Event Codes and timing
                self.state_time += dt
                CurrentEvent(self)
                
                #Blank screen between trials
                self.screen.fill(BACKGROUND_COLOR)
                #time.sleep(.3)
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
                                training = False
                                
                                self.cat = 0
                                self.length = 0
                                self.theta = 0
                                self.resp = 0
                                self.DTcorrect=0
                                self.DTrt = 0
                                
                                #TRIAL_START = True
                                TRIAL_START = False
                                STIMULUS = False
                                FEEDBACK = False
                                ITI = False
                                TOO_SLOW = False
                                INVALID_KEY = False
                                DUAL_TASK_R =False
                                DUAL_TASK_P = False
                                DUAL_TRAINING_T= False
                                DUAL_TRAINING_1 = False
                                DUAL_TRAINING_R = False
                                DUAL_TRAINING_N = False
                                DUAL_TRAINING_END = False
                        
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
                        training = False
                        
                        self.cat = 0
                        self.length = 0
                        self.theta = 0
                        self.resp = 0
                        self.DTcorrect = 0
                        self.DTrt = 0
                        
                        TRIAL_START = False
                        STIMULUS = False
                        FEEDBACK = False
                        ITI = False
                        TOO_SLOW = False
                        INVALID_KEY = False
                        DUAL_TASK_P = False
                        DUAL_TASK_R = False
                        DUAL_TRAINING_T= False
                        DUAL_TRAINING_1 = False
                        DUAL_TRAINING_R = False
                        DUAL_TRAINING_N = False
                        DUAL_TRAINING_END = False
                        self.state_time = 0

            #Update screen
            ScreenUpdate(self)
            
if __name__ == '__main__': Game()





#old dual task P
##----------------------------------------------------------------------------------------------------------                
##                
##                #update timing
##
##
##                #### This is for the stroop dual task, we are going to go with the gilbert spatial squares n-back instead
##
##                
##                #jittering
##                #a = random.randint(-220,320)
##                #b = random.randint(-150,250)
##                #c = random.randint(-320,650)
##                #d = random.randint(-189,200)
##                e=450+a
##                f=400+b
##                g=650+c
##                h=500+d
##             
##                #get shuffled numbers
##                random.shuffle(Fontsizes)
##                random.shuffle(Numbs)
##
##                # display is a pair of pairs- [(6,18),(4,22)] a size 18pt '6' and a size 22pt '4'
##                disp_pair = [(Numbs[0],Fontsizes[0]),(Numbs[1],Fontsizes[1])]
##                dualfont1 = pygame.font.Font(None, Fontsizes[0])
##                dualfont2 = pygame.font.Font(None, Fontsizes[1])
##                text1 = dualfont1.render(str(Numbs[0]),1,(220,32,220))
##                text2 = dualfont2.render(str(Numbs[1]),1,(220,32,220))
##                
##                
##                self.draw_rectlist.append(self.screen.blit(text1, (e,f)))
##                self.draw_rectlist.append(self.screen.blit(text2, (g,h)))
##                ScreenUpdate(self)
##                disp_ls.append(disp_pair) #extend?
##--------------------------------------------------------------------------------------------------------------------------------





#################################




#old dual taskR
## old dual task
##                aa=random.randint(1,10)#for dual taskquestion
##                        
##                
##                if DUALFLAG:
##                    
##                    dualtext="NUMERICALY, which number was bigger in magnitude,\n" + ' ' + str(self.N)+ ' '+ "presentation(s) ago? \n'q'= right, 'p'= left"
##                    my_rectt = pygame.Rect((40, 40, 600, 600))
##                    text = render_textrect(dualtext, font, my_rectt, (240,80,10), (0,0,0))
##                    #I don't like this key associtation. maybe use 8 and 2?
##                    self.draw_rectlist.append(self.screen.blit(text, (50,100)))
##                    ScreenUpdate(self)
##                    #time.sleep(1)
##                    nback = disp_ls[M]
##
##                    
##                    if nback[0][0]>nback[1][0]:#selectors, shmlectors.
##                        correctresponse = 'L'
##                    else:
##                        correctresponse = 'R'
##                    
##                    if aa>5:
##                        NEXT_DUALFLAG=True
##                    else:
##                        NEXT_DUALFLAG=False
##                        
##                        #record response
##                    #self.state_time += dt
##                else:
##                    dualtext="PHYSICALY, which number was larger,\n " + ' '+ str(self.N)+' ' + " presentation(s) ago?"
##                    my_rectt = pygame.Rect((40, 40, 600, 600))
##                    text = render_textrect(dualtext, font, my_rectt, (227,146,84), (0,0,0))
##                    self.draw_rectlist.append(self.screen.blit(text, (50,100)))
##                    ScreenUpdate(self)
##                   # time.sleep(.5)
##                    
##                    if nback[0][1]>nback[1][1]:
##                        correctresponse = 'L'
##                    else:
##                        correctresponse = 'R'
##                    if aa>5:
##                        NEXT_DUALFLAG = True
##                    else:
##                        NEXT_DUALFLAG = False
##                    


