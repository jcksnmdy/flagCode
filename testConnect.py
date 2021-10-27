import time
import urllib.request

import serial

ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
ser.flush()
ser.write(b"" + "(255.0, 255.0, 255.0)(255.0, 255.0, 0.0)(255.0, 255.0, 0.0)".encode('ascii') + "\n".encode('ascii'))




print("Pausing for 15 seconds")
time.sleep(15)

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + "(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        return True
    except:
        ser.write(b"" + "(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        return False
# test
while not connect():
    time.sleep(1)
    print("no internet!")

print("Internet Found! Getting new code")
        ser.write(b"" + str(df.loc[(5),flag + ' Left']).encode('ascii') + str(df.loc[(5),flag + ' Left']).encode('ascii') + "(0.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))