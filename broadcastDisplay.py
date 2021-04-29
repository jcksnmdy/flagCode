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
    