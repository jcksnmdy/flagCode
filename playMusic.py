import pandas as pd
import os
import time
import threading
import paho.mqtt.client as mqtt
import sys
import socket
sys.path.append('/home/pi/Desktop/globals/')
#sys.path.append('/home/pi/Desktop/globals/')
from constants import path, arduinoNum, globalDelay, flag, knockColor
#!/usr/bin/env python3
import serial
import time
print(flag)
print("Pausing for 15 seconds")
time.sleep(15)
import urllib.request
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False
# test
if connect():
    print("connected") 
else:
    print("no internet!")
    try:
        ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
        ser.flush()
    except OSError:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.flush()
    ser.write(b"(255.0, 0.0, 255.0)\n")
    time.sleep(60)
    if connect():
        print("connected") 
    else:
        print("No connection")

time.sleep(3)
MQTT_SERVER = "192.168.1.119"
delay = 0.0618

color = flag
knockColorRed = knockColor


try:
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser.flush()
except OSError:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

MQTT_PATH = "test_channel"


ip_address = '';
def get_ip_address():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def setStatus(stat):
    global color
    color = stat

def getStatus(stat):
    global color
    return flag+"Status:"+color

df = pd.read_excel(path + "/flagCode/colorCode.xlsx")
print(str(df.loc[(5),flag + ' Left']) + " " + str(df.loc[(5),flag + ' Middle']) + " " + str(df.loc[(5),flag + ' Right']))

listenBall = threading.Thread(group=None, target=getStatus, name=None)
songCode = pd.read_excel(path + "/flagCode/song" + str(1) + ".xlsx")

def loadSong(num):
	global songCode
	songCode = pd.read_excel(path + "/flagCode/song" + str(num) + ".xlsx")

def play(num):
    global delay, songCode
    ser.flush()
    ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
    print("Programmed song playing. Programmed song count: " + str(num) + ". Song index: " + str(num))
    i = 0
    while (i < len(songCode)):
        ser.write(b"" + str(songCode.loc[(i),flag + ' Left']).encode('ascii') + str(songCode.loc[(i),flag + ' Middle']).encode('ascii') + str(songCode.loc[(i),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        line = ser.readline().decode('utf-8').rstrip()
        #print("Received:" + str(line))
        time.sleep(delay)

        i+=1
    ser.flush()
    os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "Done"')
    print("Done")

countHits = 2
def listenHitHelper():
    global done
    while done == False:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(0.1)
        if ("HIT" in line):
            print("I've been impaled")
            os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "hit"')
            print(line)
            done = True

def listenHitHelperRepeating():
    global done
    while done == False:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(0.1)
        if ("HIT" in line):
            print("I've been impaled")
            os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "hit"')
            print(line)

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
    global countHits, readying, listenBall
    countHits = knockColorRed
    ser.flush()
    global done
    done = False
    readying = False
    listenBall = threading.Thread(group=None, target=listenHitHelperC, name=None)
    listenBall.start()
    prevCount = -1
    while readying == False:
        if (countHits%2==0):
            ser.write(b"" + "(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
            setStatus("rK")
            if (countHits != prevCount):
                os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m ' + flag + "Status:rK")
                prevCount = countHits
        else:
            ser.write(b"" + "(0.0, 0.0, 255.0)(0.0, 0.0, 255.0)(0.0, 0.0, 255.0)".encode('ascii') + "\n".encode('ascii'))
            setStatus("bk")
            if (countHits != prevCount):
                os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m ' + flag + "Status:bK")
                prevCount = countHits
        time.sleep(0.3)
    ser.flush()
    print("done")

def listenHitCapture():
    global countHits, done, readying, listenBall
    readying = False
    countHits = 0
    ser.flush()
    done = False
    listenBall = threading.Thread(group=None, target=listenHitHelperC, name=None)
    listenBall.start()
    while readying == False:
        print(str(countHits))
        if (countHits == 0):
            ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
            setStatus(flag)
        if (countHits == 1):
            ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + "(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
            setStatus(flag)
        if (countHits == 2):
            ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + "(0.0, 0.0, 0.0)".encode('ascii') + "(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
            setStatus(flag)
        if (countHits == 3):
            os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "got:"'+flag)
            ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
            setStatus("off")
            done = True
            readying = True
        time.sleep(0.2)
    ser.flush()
    listenBall.join()
    print("done")

def listenHit():
    ser.flush()
    global done, readying, listenBall
    done = False
    readying = False
    listenBall = threading.Thread(group=None, target=listenHitHelperRepeating, name=None)
    listenBall.start()
    while readying == False:
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        setStatus(flag)
        
    os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -r -n')
    ser.flush()
    listenBall.join()
    print("done")
    #client2.loop_stop()

def update():
    line = ser.readline().decode('utf-8').rstrip()
    ser.flush()
    return line

def listenHitPopup():
    global listenBall, done
    ser.flush()
    done = False
    listenBall = threading.Thread(group=None, target=listenHitHelper, name=None)
    listenBall.start()
    while done == False:
        print("popping")
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str("(255.0, 255.0, 255.0)").encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str("(255.0, 255.0, 255.0)").encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + str("(255.0, 255.0, 255.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
    ser.flush()
    listenBall.join()
    print("done")

def listenHitTarget():
    global listenBall
    ser.flush()
    global done
    done = False
    listenBall = threading.Thread(group=None, target=listenHitHelper, name=None)
    listenBall.start()
    while done == False:
        print("Targeting")
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),'off']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
    ser.flush()
    listenBall.join()
    print("done")
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    time.sleep(1)
    ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + "\n".encode('ascii'))

    time.sleep(1)
    ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + "\n".encode('ascii'))

    address = get_ip_address()
    print("Returning connected: " + address)
        
    ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + "\n".encode('ascii'))
    time.sleep(3)
    line = ser.readline().decode('utf-8').rstrip()
    if (len(line)>5):
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m ' + str(flag+":Ready:"+str(address)))
    else:
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m ' + str(flag+":arduinoNotConnected:"+str(address)))
        
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
        
knockoutCall = threading.Thread(group=None, target=listenHitKnockout, name=None)
targetingCall = threading.Thread(group=None, target=listenHitTarget, name=None)
targetingCallRepeat = threading.Thread(group=None, target=listenHit, name=None)
targetingCallCapture = threading.Thread(group=None, target=listenHitCapture, name=None)
popupCall = threading.Thread(group=None, target=listenHitPopup, name=None)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global popupCall, listenBall, delay, readying, done, targetingCallRepeat, targetingCallCapture, targetingCall, knockoutCall
    print(msg.topic+" "+str(msg.payload))
    if ("update" in str(msg.payload)):
        if ("HIT" in update()):
            os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "hit"')
    if("song" in str(msg.payload)):
        Rmsg = str(msg.payload)
        print("Song" + str(Rmsg[6]))
        play(int(Rmsg[6]))

    if("load" in str(msg.payload)):
        Rmsg = str(msg.payload)
        print("Loading"  + str(Rmsg[6]))
        loadSong(int(Rmsg[6]))

    if("wait" in str(msg.payload)):
        print("Waiting to be hit")
        ser.write(b"" + "modeing".encode('ascii') + "\n".encode('ascii'))
        #listenHit()
        ser.write(b"" + "(255.0, 255.0, 255.0)(255.0, 255.0, 255.0)(255.0, 255.0, 255.0)".encode('ascii') + "\n".encode('ascii'))
        targetingCallRepeat = threading.Thread(group=None, target=listenHit, name=None)
        targetingCallRepeat.start()
    if("targetGame" + flag[0:1].upper() in str(msg.payload)):
        print("Waiting to be hit Target")
        ser.write(b"" + "modeing".encode('ascii') + "\n".encode('ascii'))
        ser.write(b"" + "(255.0, 255.0, 255.0)(255.0, 255.0, 255.0)(255.0, 255.0, 255.0)".encode('ascii') + "\n".encode('ascii'))
        targetingCall = threading.Thread(group=None, target=listenHitTarget, name=None)
        targetingCall.start()
    if("capture" in str(msg.payload) and "hit" not in str(msg.payload)):
        print("Waiting to be hit Capture")
        ser.write(b"" + "modeing".encode('ascii') + "\n".encode('ascii'))
        ser.write(b"" + "(255.0, 255.0, 255.0)(255.0, 255.0, 255.0)(255.0, 255.0, 255.0)".encode('ascii') + "\n".encode('ascii'))
        targetingCallCapture = threading.Thread(group=None, target=listenHitCapture, name=None)
        targetingCallCapture.start()
    if("knockout" in str(msg.payload)):
        print("Waiting to be hit Knockout")
        ser.write(b"" + "modeing".encode('ascii') + "\n".encode('ascii'))
        ser.write(b"" + "(255.0, 255.0, 255.0)(255.0, 255.0, 255.0)(255.0, 255.0, 255.0)".encode('ascii') + "\n".encode('ascii'))
        knockoutCall = threading.Thread(group=None, target=listenHitKnockout, name=None)
        knockoutCall.start()
    if("stop" in str(msg.payload)):
        print("Stopping")
        ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        ser.write(b"" + "notMode".encode('ascii') + "\n".encode('ascii'))
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -r -n')
        readying = True
        done = True
        readying = True
        done = True
        time.sleep(0.01)
        if (targetingCall.is_alive()):
            targetingCall.join()
        if (knockoutCall.is_alive()):
            knockoutCall.join()
        if (targetingCallRepeat.is_alive()):
            targetingCallRepeat.join()
        if (targetingCallCapture.is_alive()):
            targetingCallCapture.join()
        if (popupCall.is_alive()):
            popupCall.join()
        if (listenBall.is_alive()):
            listenBall.join()
        if (listenBall.is_alive()):
            listenBall.join()
        if (listenBall.is_alive()):
            listenBall.join()
    if (("restart:"+flag) in str(msg.payload)):
        print("Restarting: " + flag)
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "Confirming Restart: "' + str(flag))
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -r -n')
        os.system('sudo reboot')
    if("shutdown" in str(msg.payload)):
        print("Shutting down")
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m "Confirming Shutdown: "' + str(flag))
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -r -n')
        os.system('sudo shutdown -h now')
    if("status" in str(msg.payload)):
        print("Returning status")
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m ' + str(getStatus()))

    if(("popup:"+flag) in str(msg.payload)):
        print("Pop uping")
        ser.write(b"" + "modeing".encode('ascii') + "\n".encode('ascii'))
        ser.write(b"" + "(255.0, 255.0, 255.0)(255.0, 255.0, 255.0)(255.0, 255.0, 255.0)".encode('ascii') + "\n".encode('ascii'))
        popupCall = threading.Thread(group=None, target=listenHitPopup, name=None)
        popupCall.start()

    if(("testSilent:"+flag) in str(msg.payload)):
        address = get_ip_address()
        print("Returning connected: " + address)
        
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(3)
        line = ser.readline().decode('utf-8').rstrip()
        if (len(line)>5):
            os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m ' + str(flag+":Ready:"+str(address)))
        else:
            os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m ' + str(flag+":arduinoNotConnected:"+str(address)))
        
    if(("test:"+flag) in str(msg.payload)):
        print("Returning connected")
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),'off']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),'off']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),'off']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),'off']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + "(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),'off']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)

        ser.write(b"" + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),'off']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)

        ser.write(b"" + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),'off']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)

        ser.write(b"" + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),'off']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)

        ser.write(b"" + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Middle']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),'off']).encode('ascii') + str("(0.0, 0.0, 0.0)").encode('ascii') + str(df.loc[(5),flag + ' Right']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.1)
        os.system('mosquitto_pub -h ' + MQTT_SERVER + ' -t test_channel -m ' + str(flag+":connected:"))
    if ("delay:" in str(msg.payload)):
        delay = msg.payload[6]
    if(("hit" + flag) in str(msg.payload)):
        print("hitting from computer")
        ser.write(b"HIT" + "\n".encode('ascii'))
    elif(flag in str(msg.payload) and "Status" not in str(msg.payload)):
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



"""
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=myprogram
Exec=lxterminal -e bash -c '/home/pi/Desktop/flagCode/runListeningAction;$SHELL'
Terminal=true
"""

