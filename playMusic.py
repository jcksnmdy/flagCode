import pandas as pd
import pygame
import os
import time
import random
import signal
import pygame_widgets

numInPlaylist = 1

def play(num):
    print("Programmed song playing. Programmed song count: " + str(num) + ". Song index: " + str(num))
    i = 5
    df = pd.read_excel("/home/pi/Desktop/coreLightShow/songs/song" + str(num) + ".xlsx")
    pygame.mixer.music.load("/home/pi/Desktop/coreLightShow/songs/song" + str(num) + ".mp3")
    while (i < len(df)):
        print("Hy")