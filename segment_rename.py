import os
import sys

path = sys.argv[1]
all_segments  = os.listdir(path)

for segment in all_segments:
    #print "old name:", segment

    name, suffix = os.path.splitext(segment)
    if suffix != ".ts":
        continue

    [vid, sid, res] = name.split('_')
    [wd, ht] = res.split('x')
    new_name = vid + "_" + wd + "_" + ht + "_" + \
            "df" + "_" + sid + suffix
    #print new_name
    old_path = os.path.join(path, segment)
    print old_path
    new_path = os.path.join(path, new_name)
    print new_path
    os.rename(old_path, new_path)
