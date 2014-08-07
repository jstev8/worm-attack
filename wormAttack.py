#Worm Attack
#Created on: July 10, 2014
#Update on: August 7, 2014
#TO DO: make separate file for high score

import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

 #             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
SLATE  = ( 40,  40,  40)
BLUE      = ( 51, 153, 255)
BROWN     = (132, 109,  16)
DARKBROWN = ( 114, 86,  21)
GRASSGREEN = ( 41, 213, 21) 
BGCOLOR   = BLUE
GAMEBG    = GRASSGREEN

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 


def main():
    global FPSCLOCK, DISPLAY, BASICFONT, gameScore, HIGHSCORE
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Worm Attack')
    HIGHSCORE = []
    
    menuScreen()
    
    while True: #main game loop
        runGame()
        gameOverScreen()
        


def runGame():
    global gameScore
    #set a random start point
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y':starty},
                  {'x': startx - 1, 'y':starty},
                  {'x':startx - 2,  'y':starty}]
    direction = RIGHT
    
    #start the apple in a random place
    apple = getRandomLocation()
    
    while True: #main gmae loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key ==K_a) and direction!= RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key==K_d) and direction !=LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_p:
                    pauseGame()
        
        #check if worm hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return #game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return #game over
        
        #check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation() # set new apple
        else:
            del wormCoords[-1] #remove worm's tail 
            
        #move the worm
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        drawBackground()
        drawWorm(wormCoords)
        drawApple(apple)
        gameScore = len(wormCoords) - 3
        drawScore(gameScore)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        

def pauseGame():
    DISPLAY.fill(RED)
    pauseSurf = BASICFONT.render('Press p again to return to the game', True, WHITE)
    pauseRect = pauseSurf.get_rect()
    pauseRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    pygame.display.update()
    pygame.time.wait(2000)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play', True, SLATE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAY.blit(pressKeySurf, pressKeyRect)


def isKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def menuScreen():
    titleFont = pygame.font.SysFont('calibri', 70)
    titleSurf1 = titleFont.render('Worm Attack', True, WHITE)
    
    downMove = 1
    rightMove = 10
    while True:
        DISPLAY.fill(BGCOLOR)
        DISPLAY.blit(titleSurf1, (WINDOWWIDTH/2 - 50, WINDOWHEIGHT/2-50))
        lastSeg = drawBigWorm(rightMove, downMove)
        if (lastSeg.top > WINDOWHEIGHT + 10):
            downMove = 1
            rightMove = rightMove + 60
            pygame.time.wait(1000)
        if (rightMove > WINDOWWIDTH/3):
            rightMove = 10
        drawPressKeyMsg()
        
        if isKeyPress():
            pygame.event.get() 
            return 
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        downMove += 10


def drawBigWorm(topx, topy):
    pygame.draw.rect(DISPLAY, DARKBROWN, (topx, topy - 50, 50, 50))
    pygame.draw.rect(DISPLAY, BROWN, (topx + 5, topy  -45, 40, 40))
    pygame.draw.rect(DISPLAY, DARKBROWN, (topx, topy - 100, 50, 50))
    pygame.draw.rect(DISPLAY, BROWN, (topx+5, topy - 95 , 40, 40))   #-5 + 5-
    
    lastSegment = pygame.draw.rect(DISPLAY, DARKBROWN, (topx, topy - 150, 50, 50))
    pygame.draw.rect(DISPLAY, BROWN, (topx + 5, topy - 145, 40, 40))# -100 + 5
    return lastSegment


def getRandomLocation():
    #Used for coordinates of apple
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def gameOverScreen():
    global HIGHSCORE, gameScore
    #Game Over sign
    gameOverFont = pygame.font.SysFont('calibri', 70)
    gameSurf = gameOverFont.render('Game Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    
    #Draw High Score    
    drawHighScore(gameScore)
    DISPLAY.blit(gameSurf, gameRect)
    pygame.display.update()
    
    while True:
        if isKeyPress():
            pygame.event.get() 
            return

def drawHighScore(score):
    #drawn for end of game
    global HIGHSCORE
    startTime = pygame.time.get_ticks() #milliseconds since pygame.init() was called
    scoreTime = str(startTime/60) + " min " + str(startTime%60) + " sec "
    
    if (len(HIGHSCORE) == 0):
        HIGHSCORE = [{'score': gameScore, 'time': scoreTime}]
    else:
        i = 0
        while (i <= len(HIGHSCORE)-1):
            #ensure scores are in order highest to lowest in HIGHSCORE list
            if (HIGHSCORE[i]['score'] <= gameScore):
                HIGHSCORE.insert(i, {'score': gameScore, 'time': scoreTime})
                i = i + 1
            i = i + 1
    
    #TO DO: save scores in separate file 
    f = open('highscores.txt', 'r+')
    firstline = f.readline()
    linesRead = 1
    lastline = f.readline()
    while lastline != '':
        linesRead = linesRead + 1
        #parsing string
        #get score from string
        #compare score to gameScore, if score is less than gameScore then,
        #insert gameScore at that location and move everything else down and
        #return so that while loop will stop    --lastline = ''
        #else lastline = f.readline
    f.close()
    
    
    #display only highest score 
    highScoreFont = pygame.font.SysFont('calibri', 40)
    displayScore = "Highest Score: " + str(HIGHSCORE[0]['score'])
    highScoreSurf = highScoreFont.render(displayScore, True, WHITE)
    highScoreRect = highScoreSurf.get_rect()
    highScoreRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    
    #display only current Score
    showCurrentScore = "Score: " + str(gameScore)
    scoreSurf = highScoreFont.render(showCurrentScore, True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 3)
    
    DISPLAY.blit(scoreSurf, scoreRect)
    DISPLAY.blit(highScoreSurf, highScoreRect)


def drawBackground():
    DISPLAY.fill(GAMEBG)    
    leafGrass = pygame.image.load('leafGrassSmall.png')
    #Top Left
    DISPLAY.blit(leafGrass, (0.1*WINDOWWIDTH, 0.08*WINDOWHEIGHT))
    DISPLAY.blit(leafGrass, (0.3*WINDOWWIDTH, 0.2*WINDOWHEIGHT))
    DISPLAY.blit(leafGrass, (0.02*WINDOWWIDTH, 0.38*WINDOWHEIGHT))
    
    #Center
    DISPLAY.blit(leafGrass, (0.39*WINDOWWIDTH, 0.43*WINDOWHEIGHT))
    DISPLAY.blit(leafGrass, (0.5*WINDOWWIDTH, 0.7*WINDOWHEIGHT))
    
    #Top Right
    DISPLAY.blit(leafGrass, (0.9*WINDOWWIDTH, 0.1*WINDOWHEIGHT))
    DISPLAY.blit(leafGrass, (0.6*WINDOWWIDTH, 0.3*WINDOWHEIGHT))
    DISPLAY.blit(leafGrass, (0.53*WINDOWWIDTH, 0.02*WINDOWHEIGHT))
    DISPLAY.blit(leafGrass, (0.73*WINDOWWIDTH, 0.5*WINDOWHEIGHT))
    #Bottom Left
    DISPLAY.blit(leafGrass, (0.17*WINDOWWIDTH, 0.74*WINDOWHEIGHT))
    DISPLAY.blit(leafGrass, (0.005*WINDOWWIDTH, 0.87*WINDOWHEIGHT))
    
    #Bottom Right
    DISPLAY.blit(leafGrass, (0.93*WINDOWWIDTH, 0.82*WINDOWHEIGHT))
    DISPLAY.blit(leafGrass, (0.652*WINDOWWIDTH, 0.638*WINDOWHEIGHT))
    DISPLAY.blit(leafGrass, (0.782*WINDOWWIDTH, 0.927*WINDOWHEIGHT))


def drawScore(score):
    #drawn during game play
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAY.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.draw.rect(DISPLAY, DARKBROWN, (x, y, CELLSIZE, CELLSIZE))
        innerSegment = pygame.draw.rect(DISPLAY, BROWN, (x + 2, y + 2, CELLSIZE - 4, CELLSIZE - 4))
        
        
def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    anApple = pygame.image.load('appleSmall.png')
    DISPLAY.blit(anApple, (x, y))


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
