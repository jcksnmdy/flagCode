import pandas as pd
import os
import time
from broadcastDisplay import toColor
import paho.mqtt.client as mqtt
import sys
sys.path.append('/home/pi/Desktop/globals/')
from constants import path, arduinoNum
#!/usr/bin/env python3
import serial
import time

ser = serial.Serial('/dev/ttyACM' + arduinoNum, 9600, timeout=1)
ser.flush()

MQTT_SERVER = "192.168.1.119"
flag = "red"

MQTT_PATH = "test_channel"


def play(num):
    print("Programmed song playing. Programmed song count: " + str(num) + ". Song index: " + str(num))
    i = 5
    df = pd.read_excel(path + "/flagCode/song" + str(num) + ".xlsx")
    while (i < len(df)):
        ser.write(b"" + toColor(df.loc[(i),flag + ' Left']) + "\n")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(0.01)
        print(str(i) + " " + str(df.loc[(i),flag + ' Left']))
        i+=3
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
