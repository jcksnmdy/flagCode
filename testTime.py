import datetime
import time
delay = 0.0615
now = time.time()
earlier = time.time()

i = 0
while True:
    earlier = time.time()
    while (now-earlier) < delay:
        now = time.time()
        #print(earlier-now)
    print("RUN: " + str(i))
    i+=1

# while True:
#     time.sleep(0.0615)
#     print("RUN" + str(i))
#     i+=1