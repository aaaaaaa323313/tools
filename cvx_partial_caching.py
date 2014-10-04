import os
import sys
import math
import redis
import random
import shutil
import scipy.io
from gurobipy import *

def average_arrival(rate, popularity, seg, seg_num):
    return rate * popularity * math.exp((-4.6) * seg / seg_num)


content_num = 1000

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
format_trans_price = [i * (0.105 / 3600) for i in [0.5, 0.45, 0.39, 0.37]]   #0.105
trans_latency = [2.91, 2.87, 2.27, 1.96]
storage_p = 0.0300 / 1000


r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set("content_num", content_num)

all_seg_num = 0
cached_seg_num = 0
uncached_seg_num = 0

storage_prices = []
storage_cost = []
computing_prices = []
computing_cost = []
seg_req_rate = []
segments = []

m = Model("cvx123")

for i in range(0, content_num):
    content = i
    content = str(content)
    new_dir = os.path.join(dest_path, content)
    if not os.path.exists(new_dir):
        #shutil.rmtree(new_dir)
        os.makedirs(new_dir)

    seg_num = seg_nums[0][i];
    #print "new content id:", content
    #print "segment number:", seg_num
    #print "------------------------"
    #set the information of request rate and segment number
    key = "seg_num_" + content
    val = seg_num
    r.set(key, val)

    key = "req_rate_" + content
    rate = request_rates[i][19] * 4
    r.set(key, rate)

    #copy the original video content into the dir
    for seg in range(seg_num):
        seg = str(seg)
        new_seg = content + "_" + seg + ".ts"
        new_seg = os.path.join(new_dir, new_seg)

        old_seg = source_id + "_" + seg + ".ts"
        old_seg = os.path.join(source_path, old_seg)

        if os.path.isfile(new_seg):
            pass
        else:
            shutil.copy2(old_seg, new_seg)

    resolutions = ['1280_720', '854_480', '640_360', '426_240']

    for j in range(0, format_num):
        for seg in range(seg_num):

            all_seg_num = all_seg_num + 1

            seg_stor_p = format_storage_size[j] * storage_p
            seg_tran_p = format_trans_price[j] * average_arrival(rate, format_popular[j], seg, seg_num)

            seg_stor_c = format_storage_size[j]
            seg_tran_c = average_arrival(rate, format_popular[j], seg, seg_num) * trans_latency[j]

            storage_prices.append(seg_stor_p)
            computing_prices.append(seg_tran_p)

            storage_cost.append(seg_stor_c)
            computing_cost.append(seg_tran_c)

            seg_req_rate.append(average_arrival(rate, format_popular[j], seg, seg_num))

            seg_name = str(i) + "_" + str(j) + "_" + str(seg)

            var = m.addVar(vtype=GRB.BINARY, name=seg_name)
            segments.append(var)


pure_storage   = sum(storage_prices)
pure_computing = sum(computing_prices)
total_str_c = sum(storage_cost)
total_cmp_c = sum(computing_cost)
total_seg_rate = sum(seg_req_rate)

m.update()
m.setObjective(LinExpr(storage_prices, segments) - \
        LinExpr(computing_prices, segments) + \
        pure_computing, GRB.MINIMIZE)
m.addConstr(LinExpr(storage_cost, segments), "<=", total_str_c * 0.36, "c0")
m.addConstr((total_cmp_c - LinExpr(computing_cost, segments)) \
        / total_seg_rate, "<=", 10000000000, "c1")
m.optimize()

optimal_cost   = m.objVal


for v in m.getVars():
    #print v.varName
    [content, j, seg] = v.varName.split('_')
    j = int(j)
    seg = int(seg)
    if v.x == 1.0:
        cached_seg_num = cached_seg_num + 1

        new_seg = content + '_' + resolutions[j] + '_' + 'df' + '_' + str(seg) + '.ts'
        new_seg = os.path.join(new_dir, new_seg)

        old_seg = source_id + "_" + resolutions[j] + '_' + 'df' + '_' + str(seg) + ".ts"
        old_seg = os.path.join(source_path, old_seg)

        if os.path.isfile(new_seg):
            pass
        else:
            shutil.copy2(old_seg, new_seg)

    elif v.x == 0.0:
        uncached_seg_num = uncached_seg_num + 1
        new_seg = content + '_' + resolutions[j] + '_' + 'df' + '_' + str(seg) + '.ts'
        new_seg = os.path.join(new_dir, new_seg)
        if os.path.isfile(new_seg):
            os.remove(new_seg)

    else:
        print "solution error"
        sys.exit()

print '-------------------------------'
print 'segment cached percentage:', cached_seg_num * 1.0 / all_seg_num
print 'The cost Reduction percentage:', (pure_storage - optimal_cost) / pure_storage


