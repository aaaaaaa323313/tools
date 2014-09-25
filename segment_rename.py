import os

path = sys.argv[1]
all_segments  = os.listdir(path)

for segment in all_segments:
    print segment
    name, suffix = os.path.splitext(segment)
    print name
    print suffix

