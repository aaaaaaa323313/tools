import socket
import time
import os
import uuid


def get_cpu_usage():
    total = 0
    times = 0
    lines = os.popen('mpstat -P ALL 1 3').readlines()
    for line in lines:
        if line.find("all") < 0:
            continue
        str = line.split(' ')
        cnt = len(str)
        try:
            total = total + float(str[cnt-1])
        except:
            return -1
        times = times + 1
    if times == 0:
        return -1

    cpu_usage = total/times
    return cpu_usage


def get_net_usage():
    totalin     = 0
    totalout    = 0
    times       = 0
    lines = os.popen('sar -n DEV 1 3').readlines()
    for line in lines:
        if line.find("eth") < 0:
            continue
        str = line.split(' ')
        item = []
        for i in str:
            if i != '':
                item.append(i)
        totalin = totalin + float(item[5])
        totalout = totalout + float(item[6])
        times = times + 1

    speed_in	= totalin/times
    speed_out	= totalout/times

    return (speed_in, speed_out)


def get_disk_usage():
    total = 0
    times = 0

    lines = os.popen('iostat -x 1 3').readlines()
    for line in lines:
        if line.find("sd") < 0:
            continue
        str = line.split(' ')
        try:
            if str[0].find("sd") < 0:
                continue
        except:
            return -1

        cnt = len(str)
        try:
            total = total + float(str[cnt-1])
        except:
            return -1
        times = times + 1

    if times == 0:
        return -1

    disk_usage = total/times
    return disk_usage


count       = 0
ave_cpu     = 0.0
ave_disk    = 0.0
ave_net_in  = 0.0
ave_net_out = 0.0


while True:

    try:
        cpu_usage = get_cpu_usage( )
        ave_cpu += cpu_usage
        cpu_info = "%s:%.2f; " % ("cpu", cpu_usage)

        speed_in, speed_out = get_net_usage( )
        ave_net_in  += speed_in
        ave_net_out += speed_out
        net_info = "%s:%.2f; %s:%.2f; " % ("net_speed_in", speed_in, "net_speed_out", speed_out)

        disk_usage = get_disk_usage( )
        ave_disk += disk_usage
        disk_info = "%s:%.2f; " % ("disk_usage", disk_usage)


        msg = cpu_info + net_info + disk_info
        print msg
        count += 1

        if count > 0:
            print 'ave cpu:%.2f'        %   (ave_cpu / count)
            print 'ave disk:%.2f'       %   (ave_disk / count)
            print 'ave net in:%.2f'     %   (ave_net_in / count)
            print 'ave net out:%.2f'    %   (ave_net_out / count)

    except:
        continue



