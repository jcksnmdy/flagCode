import time
import urllib.request

import serial

try:
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser.flush()
except OSError:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()ser.flush()


ser.flushInput()
ser.flushOutput()

ser.write(b"" + "(255.0, 255.0, 255.0)(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
ser.write(b"" + "(255.0, 255.0, 255.0)(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
ser.write(b"" + "(255.0, 255.0, 255.0)(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))


print("Pausing for 15 seconds")
time.sleep(15)

line = ser.readline().decode('utf-8').rstrip()
line = ser.readline().decode('utf-8').rstrip()
line = ser.readline().decode('utf-8').rstrip()
print(line)

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        ser.write(b"" + "(255.0, 255.0, 255.0)(0.0, 255.0, 0.0)(0.0, 255.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        ser.write(b"" + "(255.0, 255.0, 255.0)(0.0, 255.0, 0.0)(0.0, 255.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        ser.write(b"" + "(255.0, 255.0, 255.0)(0.0, 255.0, 0.0)(0.0, 255.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.01)
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        return True
    except:
        ser.write(b"" + "(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        ser.write(b"" + "(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        ser.write(b"" + "(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)(255.0, 0.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
        time.sleep(0.01)
        line = ser.readline().decode('utf-8').rstrip()
        print(line) 
        return False
# test
while not connect():
    time.sleep(1)
    print("no internet!")

print("Internet Found! Getting new code")
ser.write(b"" + "(255.0, 255.0, 255.0)(0.0, 255.0, 0.0)(0.0, 255.0, 0.0)".encode('ascii') + "\n".encode('ascii'))
time.sleep(0.01)
line = ser.readline().decode('utf-8').rstrip()
print(line)
