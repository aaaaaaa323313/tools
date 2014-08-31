import os
import sys
import time

ts_num = 0
trans_time = 0


path = sys.argv[1]
resolution = sys.argv[2]

for file_name in os.listdir(path):
    input_file = os.path.join(path, file_name)
    name, suffix = os.path.splitext(input_file)
    if suffix != ".ts" or resolution in name:
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


