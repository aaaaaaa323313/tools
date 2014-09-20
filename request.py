import redis
import pycurl
import cStringIO

host_ip = "127.0.0.1"
host_port = "80"



r = redis.StrictRedis(host='localhost', port=6379, db=0)
content_num = r.get('content_num')
content_num = int(content_num)

for i in range(content_num):
    content_name = 'content' + '_' + str(i)
    seg_num = r.get(content_name)
    seg_num = int(seg_num)
    for j in range(seg_num):
        url = "http://" + host_ip + ":" + host_port + "/" + \
                str(i) + "_" + str(j) + ".ts"
        print url

    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()

    #m = hashlib.md5()
    #m.update(buf.getvalue())
    buf.close()
    #print m.hexdigest()
