import hashlib
import pycurl
import cStringIO

buf = cStringIO.StringIO()
c = pycurl.Curl()
c.setopt(pycurl.FOLLOWLOCATION, 1)
c.setopt(c.URL, 'http://155.69.149.26/dream_700_700_1k_012.ts')
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()

m = hashlib.md5()
m.update(buf.getvalue())
buf.close()
print m.hexdigest()
