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

    def viewing_proc(self, content, seg_num, req_rat):
        print "content id:", content
        print "segment number:", seg_num
        print "request rate:", req_rat

        p = req_rat / 30.0 / 24.0 / 6.0

        if p > 1:
            times = int(p)
            print times
        else:
            print p



    def run(self):
        r = redis.Redis(host='192.168.0.9', port=6379, db=0)
        while True:
            for content in self.play_list:
                cmd = 'seg_num_' + str(content)
                seg_num = r.get(cmd)
                cmd = 'req_rate_' + str(content)
                req_rat = r.get(cmd)

                viewing_proc(content, seg_num, req_rat)

                time.sleep(3)


r = redis.Redis(host='192.168.0.9', port=6379, db=0)
content_num = r.get("content_num")
content_num = int(content_num)

thread_num = 2
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


