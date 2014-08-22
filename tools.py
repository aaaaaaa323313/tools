import hashlib
import pycurl
import cStringIO
from random import randrange

vid     = 'xiaoshenke'
seg_num = 849

while True:
    i = randrange(seg_num)
    no = str(i)
    url = 'http://155.69.149.26/' + vid + '_' + no + '.ts'
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
