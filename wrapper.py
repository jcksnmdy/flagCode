import pandas as pd
import os
import time
import threading
import paho.mqtt.client as mqtt
import sys
import socket
import datetime
sys.path.append('/home/pi/Desktop/globals/')
#sys.path.append('/Users/s1034274/Desktop/globals')
from constants import path, arduinoNum, globalDelay, flag, knockColor
#!/usr/bin/env python3
import serial
import time

MQTT_SERVER = "192.168.99.93"
delay = 0.0615
initDelay = 0.0615

MQTT_PATH = "test_channel"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

prepareLook = threading.Thread(group=None, target=prepareTurn, name=None)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global prepareLook
    print(msg.topic+" "+str(msg.payload))
    if("stop" in str(msg.payload)):
        print("Stopping")
        if (prepareLook.is_alive()):
            prepareLook.join() 
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
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
