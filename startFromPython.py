import pandas as pd
import os
import time
import threading
import subprocess
import paho.mqtt.client as mqtt
import sys
import serial
import signal
import time

MQTT_SERVER = "192.168.1.119"
flag = "blue"

MQTT_PATH = "test_channel"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_PATH)

proc = subprocess.Popen('python3 /home/pi/Desktop/flagCode/playMusic.py -f {0}'.format(flag), shell=True, preexec_fn=os.setsid)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global proc
    print(msg.topic+" "+str(msg.payload))
    if (("restart:"+flag) in str(msg.payload)):
        os.killpg(proc.pid, signal.SIGTERM)
        proc = subprocess.Popen('python3 /home/pi/Desktop/flagCode/playMusic.py -f {0}'.format(flag), shell=True, preexec_fn=os.setsid)

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

