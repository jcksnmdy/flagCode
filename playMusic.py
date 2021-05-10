import pandas as pd
import os
import time
import threading
from broadcastDisplay import toColor
import paho.mqtt.client as mqtt
import sys
sys.path.append('/home/pi/Desktop/globals/')
#sys.path.append('/home/pi/Desktop/globals/')
from constants import path, arduinoNum
#!/usr/bin/env python3
import serial
import time

MQTT_SERVER = "192.168.1.119"
flag = "red"

try:
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser.flush()
except OSError:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

MQTT_PATH = "test_channel"

ser.write(b"(255, 255, 255)\n")

def play(num):
    print("Programmed song playing. Programmed song count: " + str(num) + ". Song index: " + str(num))
    i = 5
    df = pd.read_excel(path + "/flagCode/song" + str(num) + ".xlsx")
    while (i < len(df)):
        print(str(i) + " Sending: " + str(df.loc[(i),flag + ' Left']) + str(df.loc[(i),flag + ' Middle']) + str(df.loc[(i),flag + ' Right']))
        ser.write(b"" + str(df.loc[(i),flag + ' Left']).encode('ascii') + str(df.loc[(i),flag + ' Middle']).encode('ascii') + str(df.loc[(i),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        #line = ser.readline().decode('utf-8').rstrip()
        #print(line)
        time.sleep(0.08)

        i+=2
    ser.flush()
    print("Done")

def listenHitHelper():
    global done
    while done == False:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(0.1)
        if ("HIT" in line):
            os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "3"')
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            #done = True

def listenHit():
    global done
    done = False
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    listenBall = threading.Thread(group=None, target=listenHitHelper, name=None)
    listenBall.start()
    while done == False:
        print("Small")
        ser.write(b"" + "(255.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        print("Med")
        ser.write(b"" + "(0.0, 0.0, 0.0)(255.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        print("Large")
        ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(255.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        print("Off")
        ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        print("Test")
        if ("HIT" in line):
            #os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "3"')
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            done = True
    ser.flush()
    print("done")
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
    if("2" in str(msg.payload)):
        print("Waiting to be hit")
        listenHit()
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
