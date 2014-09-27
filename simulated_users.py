import os
import sys
import time
import math
import random
import redis
import signal
import pycurl
import cStringIO
import threading
import subprocess
from random import randrange

class viewing_thread(threading.Thread):

    def __init__(self, play_list):
        threading.Thread.__init__(self)
        self.play_list = play_list

    def view_the_video(self, content, seg_num):
        host_ip = '192.168.0.9'
        resolutions = ['1280_720', '854_480', '640_360', '426_240']
        seg_num = int(seg_num)
        for i in range(seg_num):
            num = randrange(4)
            res = resolutions[num]
            url = "http://" + host_ip + "/" + \
                    str(content) + '_' + res + '_df_' + str(i) + '.ts'

            buf = cStringIO.StringIO()
            c = pycurl.Curl()
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(c.URL, url)
            c.setopt(c.WRITEFUNCTION, buf.write)
            c.perform()
            buf.close()

            p = math.exp((-4.6) * (i + 1) / seg_num)
            r = random.random()
            if r > p:
                break


    def viewing_proc(self, content, seg_num, req_rat):
        print "content id:", content
        print "segment number:", seg_num
        print "request rate:", req_rat

        p = int(req_rat) / 30.0 / 24.0 / 6.0

        if p > 1:
            times = int(round(p))
            for i in range(times):
                self.view_the_video(content, seg_num)
        else:
            r = random.random()
            if r < p:
                self.view_the_video(content, seg_num)



    def run(self):
        r = redis.Redis(host='192.168.0.9', port=6379, db=0)
        while True:
            for content in self.play_list:
                cmd = 'seg_num_' + str(content)
                seg_num = r.get(cmd)
                cmd = 'req_rate_' + str(content)
                req_rat = r.get(cmd)

                self.viewing_proc(content, seg_num, req_rat)

                time.sleep(3)


r = redis.Redis(host='192.168.0.9', port=6379, db=0)
content_num = r.get("content_num")
content_num = int(content_num)

thread_num = 1
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


