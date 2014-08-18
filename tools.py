import hashlib
import pycurl
import cStringIO
from random import randrange

while True:
    i = randrange(190)
    no = "%03d" % i
    url = 'http://155.69.149.26/dream_700_700_1k_' + no + '.ts'
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
