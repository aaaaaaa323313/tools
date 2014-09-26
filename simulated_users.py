import os
import sys
import time
import redis
import signal
import threading
import subprocess


r = redis.Redis(host='192.168.0.9', port=6379, db=0)
content_num = r.get("content_num")
content_num = int(content_num)



class viewing_thread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print "okay"
            time.sleep(3)


thread_num = 100
threads = []


try:
    for i in range(0, thread_num):
        t = viewing_thread()
        t.start()
        threads.append(t)
except:
    print "Error: unable to start thread"

for t in threads:
    t.join()


