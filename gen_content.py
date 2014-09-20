import os
import random
import shutil

content_num = 100

source_path = "/home/guanyu/Public/me/static/lvjuren"
source_id   = "lvjuren"
source_start = 1 * 6
source_end = 10 * 6

dest_path = "/tmp"

for content in range(0, content_num):
    content = str(content)
    new_dir = os.path.join(dest_path, content)
    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)

    os.makedirs(new_dir)

    seg_num = random.randint(source_start, source_end)
    print "new content id:", content
    print "segment number:", seg_num
    print "------------------------"


    for seg in range(seg_num):
        seg = str(seg)
        new_seg = content + "_" + seg + ".ts"
        new_seg = os.path.join(new_dir, new_seg)

        old_seg = source_id + "_" + seg + ".ts"
        old_seg = os.path.join(source_path, old_seg)

        shutil.copy2(old_seg, new_seg)


