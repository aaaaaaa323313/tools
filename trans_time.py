import os
import sys
import time

ts_num = 0
trans_time = 0

resolution = sys.argv[2]

for lists in os.listdir(sys.argv[1]):
    input_file = os.path.join(sys.argv[1], lists)
    name, suffix = os.path.splitext(input_file)
    if suffix != ".ts":
        continue

    output_file = name + "_" + resolution + ".ts"

    print input_file
    start_time = time.time()
    ts_num += 1

    cmd = "ffmpeg -y -i " + input_file + " -s " + \
            resolution + " " + output_file

    os.system(cmd)

    exec_time   = time.time() - start_time
    trans_time  += exec_time
    print "execution time:", exec_time

trans_time / ts_num


