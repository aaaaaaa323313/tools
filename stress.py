import hashlib
import pycurl
import cStringIO
from random import randrange

vid         = 'lvjuren'
seg_num     = 830
host_ip     = '155.69.146.44'
host_port   = '8090'

while True:
    i = randrange(seg_num)
    j = randrange(41)
    no = str(i)
    url = 'http://' + host_ip + ':' + host_port + '/static/' + str(j) + '/' + vid + '_' + no + '.ts'
    print url
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()

    m = hashlib.md5()
    m.update(buf.getvalue())
    buf.close()
    print m.hexdigest()
