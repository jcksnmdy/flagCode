import pandas as pd
import os
import time
from broadcastDisplay import toColor
import paho.mqtt.client as mqtt
import pyfirmata
import sys
sys.path.append('/Users/s1034274/Desktop/globals/')
from constants import path

MQTT_SERVER = "192.168.1.119"
flag = "red"

MQTT_PATH = "test_channel"

board = pyfirmata.Arduino('/dev/ttyACM0')
redLeft = board.get_pin('d:2:o')
greenLeft = board.get_pin('d:3:o')
blueLeft = board.get_pin('d:4:o')
redMid = board.get_pin('d:5:o')
greenMid = board.get_pin('d:6:o')
blueMid = board.get_pin('d:7:o')
redRight = board.get_pin('d:8:o')
greenRight = board.get_pin('d:9:o')
blueRight = board.get_pin('d:10:o')

redLeft.write(0)
greenLeft.write(0)
blueLeft.write(0)
redMid.write(0)
greenMid.write(0)
blueMid.write(0)
redRight.write(0)
greenRight.write(0)
blueRight.write(0)


def play(num):
    print("Programmed song playing. Programmed song count: " + str(num) + ". Song index: " + str(num))
    i = 5
    df = pd.read_excel(path + "/flagCode/song" + str(num) + "/" + flag + ".xlsx")
    while (i < len(df)):
        if(toColor(df.loc[(i),'red Left'])==(255,0,0)):
            print("Red")
            redLeft.write(1)
            greenLeft.write(0)
            blueLeft.write(0)
        elif(toColor(df.loc[(i),'red Left'])==(255,255,255)):
            print("White")
            redLeft.write(1)
            greenLeft.write(1)
            blueLeft.write(1)
        else:
            print("Off")
            redLeft.write(0)
            greenLeft.write(0)
            blueLeft.write(0)
        print(str(i) + " " + str(df.loc[(i),'Red Flag Left']))
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
