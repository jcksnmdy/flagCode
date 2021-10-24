import time
import urllib.request

print("Pausing for 15 seconds")
time.sleep(15)

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False
# test
while not connect():
    print("no internet!")

print("Internet Found! Getting new code")