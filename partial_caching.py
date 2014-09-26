import os
import sys
import math
import redis
import random
import shutil
import scipy.io

def average_arrival(rate, popularity, seg, seg_num):
    return rate * popularity * math.exp((-4.6) * seg / seg_num)


content_num = 100

request_rates = scipy.io.loadmat('deployed_request_rates.mat')
request_rates = request_rates['request_rate']


seg_nums = scipy.io.loadmat('deployed_seg_num.mat')
seg_nums = seg_nums['seg_num_array']


source_path = "/home/guanyu/Public/me/static/lvjuren"
source_id   = "lvjuren"

dest_path = "/home/guanyu/Public/me/static/"

format_num = 4
format_popular = [0.25, 0.25, 0.25, 0.25]
format_storage_size  = [1.93, 1.32, 1.04, 0.94]
format_trans_price = [i * (0.105 / 3600) for i in [0.5, 0.45, 0.39, 0.37]]
trans_latency = [2.91, 2.87, 2.27, 1.96]
storage_p = 0.0300 / 1000


r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set("content_num", content_num)


for i in range(0, content_num):
    content = i
    content = str(content)
    new_dir = os.path.join(dest_path, content)
    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)

    os.makedirs(new_dir)

    seg_num = seg_nums[0][i];
    print "new content id:", content
    print "segment number:", seg_num
    print "------------------------"
    #set the information of request rate and segment number
    key = "seg_num_" + content
    val = seg_num
    r.set(key, val)

    key = "req_rate_" + content
    rate = request_rates[i][0]
    r.set(key, rate)

    #copy the original video content into the dir
    for seg in range(seg_num):
        seg = str(seg)
        new_seg = content + "_" + seg + ".ts"
        new_seg = os.path.join(new_dir, new_seg)

        old_seg = source_id + "_" + seg + ".ts"
        old_seg = os.path.join(source_path, old_seg)

        shutil.copy2(old_seg, new_seg)

    resolutions = ['1280_720', '854_480', '640_360', '426_240']

    for j in range(0, format_num):
        for seg in range(seg_num):
            seg_stor_p = format_storage_size[j] * storage_p
            seg_tran_p = format_trans_price[j] * average_arrival(rate, format_popular[j], seg, seg_num)

            if seg_tran_p > seg_stor_p:
                new_seg = content + '_' + resolutions[j] + '_' + 'df' + '_' + str(seg) + '.ts'
                new_seg = os.path.join(new_dir, new_seg)

                old_seg = source_id + "_" + resolutions[j] + '_' + 'df' + '_' + str(seg) + ".ts"
                old_seg = os.path.join(source_path, old_seg)

                shutil.copy2(old_seg, new_seg)



