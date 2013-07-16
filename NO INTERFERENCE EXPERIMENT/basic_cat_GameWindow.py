#Load modules
import pygame, sys, os, math, time, datetime
from pygame.locals import *
from basic_cat_GameConstants import *

#================================================================
#These functions are general for the game, define screen, input window, and write files
#They are called within the Game class, which is the main game-loop

#This function paints every thing to the screen and cleans up objects on the screen
def ScreenUpdate(self):
    pygame.display.update(self.draw_rectlist + self.erase_rectlist)
    self.erase_rectlist = self.draw_rectlist
    for rect in self.erase_rectlist:
        self.screen.fill(BACKGROUND_COLOR, rect)
        self.draw_rectlist = []

#This is the game window that prompts the user for the subjec name and trialset
def GameInputWindow(self,DATA_DIR,TRIALSET_DIR):
    #This makes the initial window to get the trialset and data file name
    self.screen.fill(BACKGROUND_COLOR)
    pygame.display.flip()
    STILL_TYPING = True
    GET_SUBJECT = True
    GET_TRIALSET = False
    INSTRUCTIONS = False
    subject_fname = []
    trialset_fname = []
    font = pygame.font.Font('C:\\Windows\\Fonts\\georgia.ttf', 36)
    text = font.render("Subject Filename: ", 1, (255, 255, 255))
    self.draw_rectlist.append(self.screen.blit(text, (50,100)))
    text = font.render("Trial Set Filename: ", 1, (255, 255, 255))
    self.draw_rectlist.append(self.screen.blit(text, (50,200)))
    ScreenUpdate(self)
    while STILL_TYPING: #Use a while loop to grab the keys that the person presses
        if GET_SUBJECT:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    #Reprint the text already on the screen
                    text = font.render("Subject Filename: ", 1, (255, 255, 255))
                    self.draw_rectlist.append(self.screen.blit(text, (50,100)))
                    text = font.render("Trial Set Filename: ", 1, (255, 255, 255))
                    self.draw_rectlist.append(self.screen.blit(text, (50,200)))
                    if ((event.key - 48) in range(10)):
                        #They pressed a number
                        subject_fname += (NUMBERS[event.key-48])
                        subject_fname = ''.join(subject_fname)
                        subtext = font.render(str(subject_fname),1,(0,0,255))
                        self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                        ScreenUpdate(self)
                    elif ((event.key - 97) in range(26)):
                        #If they pressed another letter add it to the filename
                        subject_fname += str(LETTERS[event.key-97])
                        subject_fname = ''.join(subject_fname)
                        subtext = font.render(str(subject_fname),1,(0,0,255))
                        self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                        ScreenUpdate(self)
                    elif (event.key == K_BACKSPACE):
                        #if they hit backspace,remove the last key from the filename
                        subject_fname = subject_fname[:-1]
                        subject_fname = ''.join(subject_fname)
                        subtext = font.render(str(subject_fname),1,(0,0,255))
                        self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                        ScreenUpdate(self)
                    elif (event.key == K_RETURN):
                        fname = (DATA_DIR+'/'+str(subject_fname).replace("['","").replace("']","")+".txt")
                        if os.path.isfile(fname):
                            text = font.render("Subject File Already Exists", 1, (0, 11, 127))
                            self.draw_rectlist.append(self.screen.blit(text, (150,300)))
                            self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                            ScreenUpdate(self)
                            time.sleep(1)
                        elif not os.path.isfile(fname):
                            GET_TRIALSET = True
                            GET_SUBJECT = False
                            N=subject_fname[-1]#for the n-back: its the last digit of the trial. (default, N=1)
                    elif (event.key == K_ESCAPE):
                        pygame.display.quit()   #Closes the display
                        sys.exit()                          #Calls interrupt to end game
        if GET_TRIALSET:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    #Reprint the text already on the screen
                    text = font.render("Subject Filename: ", 1, (255, 255, 255))
                    self.draw_rectlist.append(self.screen.blit(text, (50,100)))
                    text = font.render("Trial Set Filename: ", 1, (255, 255, 255))
                    self.draw_rectlist.append(self.screen.blit(text, (50,200)))
                    if ((event.key - 48) in range(10)):
                        #They pressed a number
                        trialset_fname += (NUMBERS[event.key-48])
                        trialset_fname = ''.join(trialset_fname)
                        trialtext = font.render(str(trialset_fname),1,(0,0,255))
                        self.draw_rectlist.append(self.screen.blit(trialtext,(350,200)))
                        self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                        ScreenUpdate(self)
                    elif ((event.key - 97) in range(26)):
                        #They pressed a letter
                        trialset_fname += (LETTERS[event.key-97])
                        trialset_fname = ''.join(trialset_fname)
                        trialtext = font.render(str(trialset_fname),1,(0,0,255))
                        self.draw_rectlist.append(self.screen.blit(trialtext,(350,200)))
                        self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                        
                        ScreenUpdate(self)
                    elif (event.key == K_BACKSPACE):
                        #if they hit backspace,remove the last key from the filename
                        trialset_fname = trialset_fname[:-1]
                        trialset_fname = ''.join(trialset_fname)
                        trialtext = font.render(str(trialset_fname),1,(0,0,255))
                        self.draw_rectlist.append(self.screen.blit(trialtext,(350,200)))
                        self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                        ScreenUpdate(self)
                    elif (event.key == K_RETURN):
                        fname = (TRIALSET_DIR+'/'+str(trialset_fname).replace("['","").replace("']","")+".tgt").lower()
                        if not os.path.isfile(fname):
                            text = font.render("File Does Not Exist", 1, (255, 0, 0))
                            self.draw_rectlist.append(self.screen.blit(text, (150,300)))
                            self.draw_rectlist.append(self.screen.blit(trialtext,(350,200)))
                            self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                            ScreenUpdate(self)
                        elif os.path.isfile(fname):
                            GET_TRIALSET = False
                            STILL_TYPING = True
                            INSTRUCTIONS = True
                    elif event.key == K_ESCAPE:
                        pygame.display.quit()   #Closes the display
                        sys.exit()                          #Calls interrupt to end game
        if INSTRUCTIONS:
            screen.fill(BACKGROUND_COLOR)
            my_rect = pygame.Rect(40,40,700,700)
            text = render_textrect(INSTRUCTIONTEXT, font, my_rect, (0,0,0), (120,120,120),1)
            #text = font.render("INSTRUCTIONS", 1, (255,255,100))
            self.draw_rectlist.append(self.screen.blit(text, (SCREEN_CENTER[0]-350,SCREEN_CENTER[1]-300)))
            ScreenUpdate(self)
            time.sleep(1)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if (event.key == K_RETURN):
                        GET_TRIALSET = False
                        STILL_TYPING = False
                        INSTRUCTIONS = False
                        #return N
                    elif event.key == K_ESCAPE:
                        pygame.display.quit()   #Closes the display
                        sys.exit()
                    else:
                        GET_TRIALSET = False
                        STILL_TYPING = True
                        INSTRUCTIONS = True
                
    #Create file for saving
    data_fname = (str(subject_fname).replace("['","").replace("']","")+".txt")
    self.data_fname = data_fname
    movedata_fname = ("MOVE"+str(subject_fname).replace("['","").replace("']","")+".txt")
    self.movedata_fname = movedata_fname
    trialset_fname = (str(trialset_fname).replace("['","").replace("']","")+".tgt").lower()
    self.trialset_fname = trialset_fname
    #N=subject_fname[-1]
    self.N = int(N)
    

def WriteGameData(self,DATA_DIR,history,history_keys,):
    #Check to see if path exists, if not make it
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    #Write game data
    data_file = open(DATA_DIR+'/'+self.data_fname,'w')  #The flag 'a' will append and the 'w' will overwrite
    
    #Write header on first trial only
    #if self.trial_num == 0:
    for i in range(len(history_keys)):
        data_file.write(str(history_keys[i])+'\t')
    data_file.write('\n')

    #Write abstracted data
    for i in range(len(history['trial_num'])): #This cycles through the number of rows (or trials)
        for j in range(len(history)): #This cycles through the number of variables
            data_file.write(str(history[history_keys[j]][i])+'\t') #You use the keys to select the right variable in the dictionary and then write one variable from it
        data_file.write('\n')
    data_file.close()

    if self.trial_num == self.trialset_len-1:
        print self.trial_num
        print self.trialset_len-1
        pygame.display.quit()   #Closes the display
        sys.exit()              #Calls interrupt to end game

##    #Put in delay to make sure game gets back up to speed
##    pygame.time.delay(int(DATA_WRITE_DELAY*1000))
#=========================================================================

################WORD WRAPPING FOR INSTRUCTION SCREEN###############
####################################################################
###DAVID CLARK WROTE THE FOLLOWING

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """
    
    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface
