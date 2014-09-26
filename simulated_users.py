import os
import sys
import time
import redis
import signal
import threading
import subprocess


class viewing_thread(threading.Thread):

    def __init__(self, play_list):
        threading.Thread.__init__(self)
        self.play_list = play_list

    def run(self):
        while True:
            for content in self.play_list:
                print content
                time.sleep(3)


r = redis.Redis(host='192.168.0.9', port=6379, db=0)
content_num = r.get("content_num")
content_num = int(content_num)

thread_num = 100
threads = []

try:
    for i in range(0, thread_num):
        num_per_thread = content_num / thread_num
        play_list = range(num_per_thread * i, num_per_thread * (i + 1) )
        t = viewing_thread(play_list)
        t.start()
        threads.append(t)
except:
    print "Error: unable to start thread"

for t in threads:
    t.join()


