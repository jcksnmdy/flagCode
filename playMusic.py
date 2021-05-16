import pandas as pd
import os
import time
import threading

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
knockColorRed = 0 #Red
# knockColorRed = 1 #Blue
color = flag

try:
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser.flush()
except OSError:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

MQTT_PATH = "test_channel"

ser.write(b"(255, 255, 255)\n")

def setStatus(stat):
    global color
    color = stat

def getStatus(stat):
    global color
    return flag+"Status:"+color

def play(num):
    ser.flush()
    ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
    ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
    ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
    time.sleep(0.1)
    print("Programmed song playing. Programmed song count: " + str(num) + ". Song index: " + str(num))
    i = 5
    df = pd.read_excel(path + "/flagCode/song" + str(num) + ".xlsx")
    while (i < len(df)):
        ser.write(b"" + str(df.loc[(i),flag + ' Left']).encode('ascii') + str(df.loc[(i),flag + ' Middle']).encode('ascii') + str(df.loc[(i),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        #line = ser.readline().decode('utf-8').rstrip()
        #print("Received:" + str(line))
        time.sleep(0.08)

        i+=2
    ser.flush()
    os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "Done"')
    print("Done")

countHits = 0
def listenHitHelper():
    global done
    while done == False:
        line = ser.readline().decode('utf-8').rstrip()
        time.sleep(0.1)
        if ("HIT" in line):
            print("I've been impaled")
            os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "hit"')
            print(line)
            done = True

def listenHitHelperC():
    global done, countHits
    while done == False:
        line = ser.readline().decode('utf-8').rstrip()
        time.sleep(0.1)
        if ("HIT" in line):
            print("I've been impaled")
            os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "hit"')
            print(line)
            countHits+=1
            print(countHits)

readying = False

def listenHitKnockout():
    global countHits
    countHits = knockColorRed
    ser.flush()
    global done
    done = False
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    listenBall = threading.Thread(group=None, target=listenHitHelperC, name=None)
    listenBall.start()
    prevCount = -1
    while done == False:
        if (countHits%knockRed==0):
            ser.write(b"" + "(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
            setStatus("rK")
            if (countHits != prevCount)
                os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "redStatus:red"')
                prevCount = countHits
        else:
            ser.write(b"" + "(0.0, 0.0, 255.0)(0.0, 0.0, 255.0)(0.0, 0.0, 255.0)".encode('ascii') + "\n".encode('ascii'))
            setStatus("bk")
            if (countHits != prevCount):
                os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "redStatus:blue"')
                prevCount = countHits
        time.sleep(0.1)
    ser.flush()
    print("done")

def listenHitCapture():
    global countHits
    countHits = 0
    ser.flush()
    global done
    done = False
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    listenBall = threading.Thread(group=None, target=listenHitHelperC, name=None)
    listenBall.start()
    while done == False:
        if (countHits == 0):
            ser.write(b"" + str(df.loc[(i),flag + ' Left']).encode('ascii') + str(df.loc[(i),flag + ' Middle']).encode('ascii') + str(df.loc[(i),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
            setStatus(flag)
        elif (countHits == 1):
            ser.write(b"" + str(df.loc[(i),flag + ' Left']).encode('ascii') + str(df.loc[(i),'off']).encode('ascii') + str(df.loc[(i),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
            setStatus(flag)
        elif (countHits == 2):
            ser.write(b"" + str(df.loc[(i),flag + ' Left']).encode('ascii') + str(df.loc[(i),'off']).encode('ascii') + str(df.loc[(i),'off']).encode('ascii') + "\n".encode('ascii'))
            setStatus(flag)
        else:
            ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
            setStatus("off")
            os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "captured:"' + str(flag))
        time.sleep(0.1)
    ser.flush()
    print("done")

def listenHit():
    ser.flush()
    global done, readying
    done = False
    readying = False
    listenBall = threading.Thread(group=None, target=listenHitHelper, name=None)
    listenBall.start()
    while readying == False:
        while done == False:
            ser.write(b"" + str(df.loc[(i),flag + ' Left']).encode('ascii') + str(df.loc[(i),flag + ' Middle']).encode('ascii') + str(df.loc[(i),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
            time.sleep(0.1)
            setStatus(flag)
        done = False
        listenBall = threading.Thread(group=None, target=listenHitHelper, name=None)
        listenBall.start()
        print("Im waiting again")
    os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -r -n')
    ser.flush()
    print("done")
    #client2.loop_stop()

def update():
    line = ser.readline().decode('utf-8').rstrip()
    ser.flush()
    return line

def listenHitTarget():
    ser.flush()
    global done
    done = False
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    listenBall = threading.Thread(group=None, target=listenHitHelper, name=None)
    listenBall.start()
    while done == False:
        setStatus(flag)
        ser.write(b"" + str(df.loc[(i),flag + ' Left']).encode('ascii') + str(df.loc[(i),'off']).encode('ascii') + str(df.loc[(i),'off']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(i),'off']).encode('ascii') + str(df.loc[(i),flag + ' Middle']).encode('ascii') + str(df.loc[(i),'off']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(i),'off']).encode('ascii') + str(df.loc[(i),'off']).encode('ascii') + str(df.loc[(i),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
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
    global readying, done
    print(msg.topic+" "+str(msg.payload))
    if ("update" in str(msg.payload)):
        if ("HIT" in update()):
            os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "hit"')
    if("song" in str(msg.payload) and "1" in str(msg.payload)):
        print("Song")
        play(1)
    if("wait" in str(msg.payload)):
        print("Waiting to be hit")
        #listenHit()
        targetingCallRepeat = threading.Thread(group=None, target=listenHit, name=None)
        targetingCallRepeat.start()
    if("targetGame" + flag[0:1].upper() in str(msg.payload)):
        print("Waiting to be hit Target")
        targetingCall = threading.Thread(group=None, target=listenHitTarget, name=None)
        targetingCall.start()
    if("capture" in str(msg.payload)):
        print("Waiting to be hit Capture")
        readying = True
        done = True
        targetingCall = threading.Thread(group=None, target=listenHitCapture, name=None)
        targetingCall.start()
    if("knockout" in str(msg.payload)):
        print("Waiting to be hit Knockout")
        readying = True
        done = True
        targetingCall = threading.Thread(group=None, target=listenHitKnockout, name=None)
        targetingCall.start()
    if("stop" in str(msg.payload)):
        print("Stopping")
        ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -r -n')
        readying = True
        done = True
    if("shutdown" in str(msg.payload)):
        print("Shutting down")
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "Confirming Shutdown: "' + str(flag))
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -r -n')
        os.system('sudo shutdown -h now')
    if("status" in str(msg.payload)):
        print("Returning status")
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m ' + str(getStatus()))
    if(("hit" + flag) in str(msg.payload)):
        print("hitting from computer")
        ser.write(b"hit" + "\n".encode('ascii'))
        readying = True
        done = True
    elif(flag in str(msg.payload)):
        print("ControlMode")
        if("1" in str(msg.payload)):
            ser.write(b"" + "(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        if("2" in str(msg.payload)):
            ser.write(b"" + "(255.0, 64.0, 0.0)(255.0, 64.0, 0.0)(255.0, 64.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        if("3" in str(msg.payload)):
            ser.write(b"" + "(255.0, 128.0, 0.0)(255.0, 128.0, 0.0)(255.0, 128.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        if("4" in str(msg.payload)):
            ser.write(b"" + "(0.0, 0.0, 255.0)(0.0, 0.0, 255.0)(0.0, 0.0, 255.0)".encode('ascii') + "\n".encode('ascii'))
        if("5" in str(msg.payload)):
            ser.write(b"" + "(0.0, 255.0, 0.0)(0.0, 255.0, 0.0)(0.0, 255.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        if("6" in str(msg.payload)):
            ser.write(b"" + "(255.0, 255.0, 255.0)(255.0, 255.0, 255.0)(255.0, 255.0, 255.0)".encode('ascii') + "\n".encode('ascii'))
        if("7" in str(msg.payload)):
            ser.write(b"" + "(255.0, 0.0, 255.0)(255.0, 0.0, 255.0)(255.0, 0.0, 255.0)".encode('ascii') + "\n".encode('ascii'))
        if("8" in str(msg.payload)):
            ser.write(b"" + "(255.0, 64.0, 66.0)(255.0, 64.0, 66.0)(255.0, 64.0, 66.0)".encode('ascii') + "\n".encode('ascii'))
        if("9" in str(msg.payload)):
            ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
