import os
import sys
import time
import threading

ts_num = 0
trans_time = 0

path = sys.argv[1]
resolution = sys.argv[2]
all_files  = os.listdir(path)


class trans_thread(threading.Thread):
    def __init__(self, lock, index):
        threading.Thread.__init__(self)
        self.lock   = lock
        self.index  = index

    def run(self):

        global path
        global resolution
        global all_files

        while True:
            self.lock.acquire()
            try:
                file_name = all_files.pop()
            except:
                self.lock.release()
                break
            self.lock.release()

            input_file = os.path.join(path, file_name)
            name, suffix = os.path.splitext(input_file)
            if suffix != ".ts" or resolution in name:
                continue

            output_file = name + "_" + resolution + ".ts"
            print input_file



            cmd = "ffmpeg -y -i " + input_file + " -s " + \
                    resolution + " " + output_file


            tmp = os.popen(cmd).readlines()
            #print tmp



lock = threading.Lock()
thread_num = 2
threads = []

start_time = time.time()

try:
    for i in range(0, thread_num):
        t = trans_thread(lock, i)
        t.start()
        threads.append(t)
except:
    print "Error: unable to start thread"


for t in threads:
    t.join()


exec_time   = time.time() - start_time
#exec_time / ts_num
