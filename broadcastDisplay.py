import pandas as pd
import pygame
import os
import time

pygame.init()
pygame.font.init()
pygame.display.set_caption("Player")
font = pygame.font.Font('freesansbold.ttf', 28)
pygame.mixer.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

red = (255,0,0)
orange = (255,128,0)
blue = (0,0,255)
yellow = (255,255,0)
green = (0,255,0)
white = (255,255,255)
grey = (128,128,128)
black = (0,0,0)

def sparkleRed():
    print("Sparkling")
    setRedFlag(red, grey, grey, redFlagCenterOrig)
    time.sleep(0.2)
    setRedFlag(grey, red, grey, redFlagCenterOrig)
    time.sleep(0.2)
    setRedFlag(red, grey, grey, redFlagCenterOrig)
    time.sleep(0.2)
    setRedFlag(grey, grey, red, redFlagCenterOrig)
    time.sleep(0.2)
    setRedFlag(red, grey, grey, redFlagCenterOrig)
    time.sleep(0.2)
    setRedFlag(grey, grey, red, redFlagCenterOrig)
    time.sleep(0.2)
    setRedFlag(grey, red, grey, redFlagCenterOrig)
    time.sleep(0.2)

def pulseRed():
    while (hit == False):
        setRedFlag(red, grey, grey, redFlagCenterOrig)
        time.sleep(0.2)
        setRedFlag(grey, red, grey, redFlagCenterOrig)
        time.sleep(0.1)
        setRedFlag(grey, grey, red, redFlagCenterOrig)
        time.sleep(0.09)
        setRedFlag(grey, grey, grey, redFlagCenterOrig)
        time.sleep(1)
    
def pulseOrange():
    while (hit == False):
        setOrangeFlag(orange, grey, grey, orangeFlagCenterOrig)
        time.sleep(0.2)
        setOrangeFlag(grey, orange, grey, orangeFlagCenterOrig)
        time.sleep(0.1)
        setOrangeFlag(grey, grey, orange, orangeFlagCenterOrig)
        time.sleep(0.09)
        setOrangeFlag(grey, grey, grey, orangeFlagCenterOrig)
        time.sleep(1)

def pulseWhite():
    while (hit == False):
        setWhiteFlag(white, grey, grey, whiteFlagCenterOrig)
        time.sleep(0.2)
        setWhiteFlag(grey, white, grey, whiteFlagCenterOrig)
        time.sleep(0.1)
        setWhiteFlag(grey, grey, white, whiteFlagCenterOrig)
        time.sleep(0.09)
        setWhiteFlag(grey, grey, grey, whiteFlagCenterOrig)
        time.sleep(1)

def pulseYellow():
    while (hit == False):
        setYellowFlag(yellow, grey, grey, yellowFlagCenterOrig)
        time.sleep(0.2)
        setYellowFlag(grey, yellow, grey, yellowFlagCenterOrig)
        time.sleep(0.1)
        setYellowFlag(grey, grey, yellow, yellowFlagCenterOrig)
        time.sleep(0.09)
        setYellowFlag(grey, grey, grey, yellowFlagCenterOrig)
        time.sleep(1)

def pulseGreen():
    while (hit == False):
        setGreenFlag(green, grey, grey, greenFlagCenterOrig)
        time.sleep(0.2)
        setGreenFlag(grey, green, grey, greenFlagCenterOrig)
        time.sleep(0.1)
        setGreenFlag(grey, grey, green, greenFlagCenterOrig)
        time.sleep(0.09)
        setGreenFlag(grey, grey, grey, greenFlagCenterOrig)
        time.sleep(1)

def pulseBlue():
    while (hit == False):
        setBlueFlag(blue, grey, grey, blueFlagCenterOrig)
        time.sleep(0.2)
        setBlueFlag(grey, blue, grey, blueFlagCenterOrig)
        time.sleep(0.1)
        setBlueFlag(grey, grey, blue, blueFlagCenterOrig)
        time.sleep(0.09)
        setBlueFlag(grey, grey, grey, blueFlagCenterOrig)
        time.sleep(1)

def setRedFlag(colorInner, colorMiddle, colorOuter, space):
    spaceList = list(space)
    inner = space
    middle = (spaceList[0]-10,spaceList[1]-10,spaceList[2]+20,spaceList[3]+20)
    outer = (spaceList[0]-20,spaceList[1]-20,spaceList[2]+40,spaceList[3]+40)

    global redFlagColorCenter, redFlagCenter, redFlagColorMiddle, redFlagMiddle, redFlagColorOuter, redFlagOuter
    redFlagColorCenter = colorInner
    redFlagCenter = pygame.Rect(inner)
    redFlagColorMiddle = colorMiddle
    redFlagMiddle = pygame.Rect(middle)
    redFlagColorOuter = colorOuter
    redFlagOuter = pygame.Rect(outer)

def setOrangeFlag(colorInner, colorMiddle, colorOuter, space):
    spaceList = list(space)
    inner = space
    middle = (spaceList[0]-10,spaceList[1]-10,spaceList[2]+20,spaceList[3]+20)
    outer = (spaceList[0]-20,spaceList[1]-20,spaceList[2]+40,spaceList[3]+40)

    global orangeFlagColorCenter, orangeFlagCenter, orangeFlagColorMiddle, orangeFlagMiddle, orangeFlagColorOuter, orangeFlagOuter
    orangeFlagColorCenter = colorInner
    orangeFlagCenter = pygame.Rect(inner)
    orangeFlagColorMiddle = colorMiddle
    orangeFlagMiddle = pygame.Rect(middle)
    orangeFlagColorOuter = colorOuter
    orangeFlagOuter = pygame.Rect(outer)

def setWhiteFlag(colorInner, colorMiddle, colorOuter, space):
    spaceList = list(space)
    inner = space
    middle = (spaceList[0]-10,spaceList[1]-10,spaceList[2]+20,spaceList[3]+20)
    outer = (spaceList[0]-20,spaceList[1]-20,spaceList[2]+40,spaceList[3]+40)

    global whiteFlagColorCenter, whiteFlagCenter, whiteFlagColorMiddle, whiteFlagMiddle, whiteFlagColorOuter, whiteFlagOuter
    whiteFlagColorCenter = colorInner
    whiteFlagCenter = pygame.Rect(inner)
    whiteFlagColorMiddle = colorMiddle
    whiteFlagMiddle = pygame.Rect(middle)
    whiteFlagColorOuter = colorOuter
    whiteFlagOuter = pygame.Rect(outer)

def setYellowFlag(colorInner, colorMiddle, colorOuter, space):
    spaceList = list(space)
    inner = space
    middle = (spaceList[0]-10,spaceList[1]-10,spaceList[2]+20,spaceList[3]+20)
    outer = (spaceList[0]-20,spaceList[1]-20,spaceList[2]+40,spaceList[3]+40)

    global yellowFlagColorCenter, yellowFlagCenter, yellowFlagColorMiddle, yellowFlagMiddle, yellowFlagColorOuter, yellowFlagOuter
    yellowFlagColorCenter = colorInner
    yellowFlagCenter = pygame.Rect(inner)
    yellowFlagColorMiddle = colorMiddle
    yellowFlagMiddle = pygame.Rect(middle)
    yellowFlagColorOuter = colorOuter
    yellowFlagOuter = pygame.Rect(outer)

def setGreenFlag(colorInner, colorMiddle, colorOuter, space):
    spaceList = list(space)
    inner = space
    middle = (spaceList[0]-10,spaceList[1]-10,spaceList[2]+20,spaceList[3]+20)
    outer = (spaceList[0]-20,spaceList[1]-20,spaceList[2]+40,spaceList[3]+40)

    global greenFlagColorCenter, greenFlagCenter, greenFlagColorMiddle, greenFlagMiddle, greenFlagColorOuter, greenFlagOuter
    greenFlagColorCenter = colorInner
    greenFlagCenter = pygame.Rect(inner)
    greenFlagColorMiddle = colorMiddle
    greenFlagMiddle = pygame.Rect(middle)
    greenFlagColorOuter = colorOuter
    greenFlagOuter = pygame.Rect(outer)

def setBlueFlag(colorInner, colorMiddle, colorOuter, space):
    spaceList = list(space)
    inner = space
    middle = (spaceList[0]-10,spaceList[1]-10,spaceList[2]+20,spaceList[3]+20)
    outer = (spaceList[0]-20,spaceList[1]-20,spaceList[2]+40,spaceList[3]+40)

    global blueFlagColorCenter, blueFlagCenter, blueFlagColorMiddle, blueFlagMiddle, blueFlagColorOuter, blueFlagOuter
    blueFlagColorCenter = colorInner
    blueFlagCenter = pygame.Rect(inner)
    blueFlagColorMiddle = colorMiddle
    blueFlagMiddle = pygame.Rect(middle)
    blueFlagColorOuter = colorOuter
    blueFlagOuter = pygame.Rect(outer)

def setRedFlagSame(color, space):
    setRedFlag(color, color, color, space)

def setOrangeFlagSame(color, space):
    setOrangeFlag(color, color, color, space)

def setWhiteFlagSame(color, space):
    setWhiteFlag(color, color, color, space)

def setYellowFlagSame(color, space):
    setYellowFlag(color, color, color, space)

def setGreenFlagSame(color, space):
    setGreenFlag(color, color, color, space)

def setBlueFlagSame(color, space):
    setBlueFlag(color, color, color, space)

def resetAllFlags():
    setRedFlag(red, red, red,redFlagCenterOrig)
    setOrangeFlag(orange, orange, orange, orangeFlagCenterOrig)
    setWhiteFlag(white, white, white, whiteFlagCenterOrig)
    setYellowFlag(yellow, yellow, yellow, yellowFlagCenterOrig)
    setGreenFlag(green, green, green, greenFlagCenterOrig)
    setBlueFlag(blue, blue, blue, blueFlagCenterOrig)

def showTargets(rand, count, i):
    df = pd.read_excel("songs/song" + str(rand[count]+1) + ".xlsx")
    screen.fill([0,0,0])
    print(len(df))
    print(str(i)+ " "+ str(toColor(df.loc[(i),'Red 1'])))
    setRedFlagSame(toColor(df.loc[(i),'Red 1']), redFlagCenterOrig)
    setOrangeFlagSame(toColor(df.loc[(i),'Orange 2']), orangeFlagCenterOrig)
    setWhiteFlagSame(toColor(df.loc[(i),'White 3']), whiteFlagCenterOrig)
    setYellowFlagSame(toColor(df.loc[(i),'Yellow 4']), yellowFlagCenterOrig)
    setGreenFlagSame(toColor(df.loc[(i),'Green 5']), greenFlagCenterOrig)
    setBlueFlagSame(toColor(df.loc[(i),'Blue 6']), blueFlagCenterOrig)

    pygame.draw.rect(screen, redFlagColorCenter, redFlagCenter)  # draw button
    pygame.draw.rect(screen, orangeFlagColorCenter, orangeFlagCenter)  # draw button
    pygame.draw.rect(screen, whiteFlagColorCenter, whiteFlagCenter)  # draw button
    pygame.draw.rect(screen, yellowFlagColorCenter, yellowFlagCenter)  # draw button
    pygame.draw.rect(screen, greenFlagColorCenter, greenFlagCenter)  # draw button
    pygame.draw.rect(screen, blueFlagColorCenter, blueFlagCenter)  # draw button
    pygame.draw.rect(screen, redFlagColorMiddle, redFlagMiddle)  # draw button
    pygame.draw.rect(screen, orangeFlagColorMiddle, orangeFlagMiddle)  # draw button
    pygame.draw.rect(screen, whiteFlagColorMiddle, whiteFlagMiddle)  # draw button
    pygame.draw.rect(screen, yellowFlagColorMiddle, yellowFlagMiddle)  # draw button
    pygame.draw.rect(screen, greenFlagColorMiddle, greenFlagMiddle)  # draw button
    pygame.draw.rect(screen, blueFlagColorMiddle, blueFlagMiddle)  # draw button
    pygame.draw.rect(screen, redFlagColorOuter, redFlagOuter)  # draw button
    pygame.draw.rect(screen, orangeFlagColorOuter, orangeFlagOuter)  # draw button
    pygame.draw.rect(screen, whiteFlagColorOuter, whiteFlagOuter)  # draw button
    pygame.draw.rect(screen, yellowFlagColorOuter, yellowFlagOuter)  # draw button
    pygame.draw.rect(screen, greenFlagColorOuter, greenFlagOuter)  # draw button
    pygame.draw.rect(screen, blueFlagColorOuter, blueFlagOuter)  # draw button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            main()
    pygame.display.flip()   
    clock.tick(60)

def toColor(col):
    if (col == "red"):
        return red
    elif (col == "blue"):
        return blue
    elif (col == "green"):
        return green
    elif (col == "yellow"):
        return yellow
    elif (col == "white"):
        return white
    elif (col == "grey"):
        return grey
    elif (col == "orange"):
        return orange
    elif (col == "black"):
        return black
    elif (col == "[255, 0, 0]"):
        return red
    elif (col == "[0, 0, 255]"):
        return blue
    elif (col == "[0, 255, 0]"):
        return green
    elif (col == "[255, 255, 0]"):
        return yellow
    elif (col == "[255, 255, 255]"):
        return white
    elif (col == "[128, 128, 128]"):
        return grey
    elif (col == "[255, 128, 0]" or col == "[255, 168, 0]"):
        return orange
    elif (col == "[0, 0, 0]"):
        return black
    