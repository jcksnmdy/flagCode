import pandas as pd
import os
import time
from broadcastDisplay import toColor

numInPlaylist = 1

import paho.mqtt.client as mqtt

import pyfirmata

board = pyfirmata.Arduino('/dev/ttyACM0')
red1 = board.get_pin('d:2:o')
green1 = board.get_pin('d:3:o')
blue1 = board.get_pin('d:4:o')

red1.write(0)
green1.write(0)
blue1.write(0)

MQTT_SERVER = "192.168.1.119"
MQTT_PATH = "test_channel"


def play(num):
    print("Programmed song playing. Programmed song count: " + str(num) + ". Song index: " + str(num))
    i = 5
    df = pd.read_excel("/home/pi/Desktop/coreLightShow/songs/song" + str(num) + ".xlsx")
    while (i < len(df)):
        if(toColor(df.loc[(i),'Red 1'])==(255,0,0)):
            print("Red")
            red1.write(1)
        elif(toColor(df.loc[(i),'Red 1'])==(255,255,255)):
            print("White")
            red1.write(1)
            green1.write(1)
            blue1.write(1)
        else:
            print("Off")
            red1.write(0)
            green1.write(0)
            blue1.write(0)
        print(str(i) + " " + str(df.loc[(i),'Red 1']))
        time.sleep(0.03)
        i+=1
    print("Done")
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if("1" in str(msg.payload)):
        print("Song")
        play(1)
    # more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
