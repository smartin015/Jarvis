
class RFSerial():

  def __init__(self, ser, target):
    self.ser = ser
    self.target = target

  def snd(self, data):
    pass

  def rcv(self):
    pass
  
  def read(self, nbytes = None, timeout = 1.0):
    pass
    """
    result = ""
    if nbytes == None:
      # Read to next long pause (default 1 second)

    else:
      for i in xrange(nbytes):
        self.rcv()
    """

  def write(self, data):
    pass

  def readline(self):
    pass
      

