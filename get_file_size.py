# ls -lR static/ | grep df | grep -v lvju > tmp

f = open('tmp')
lines = f.readlines()
f.close()
total_size = 0
for line in lines:
    items = line.split(' ')
    new_items = []
    for item in items:
        if item != '':
            new_items.append(item)

    size = int(new_items[4])
    total_size += size

print total_size * 1.0 /1024/1024/1024
