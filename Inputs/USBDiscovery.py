import re
import subprocess
import config

def get_connected_usb_devices():
  #device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
  device_re = re.compile("ATTRS{serial}==\"(.+?)\"")
  df = subprocess.check_output("ls -l /dev/ttyUSB*", shell=True)
  try:
    df += subprocess.check_output("ls -l /dev/ttyACM*", shell=True, stderr=subprocess.PIPE)
  except subprocess.CalledProcessError:
    pass

  devices = {}
  for i in df.split('\n'):
    if not i:
      continue
    path = i.split()[-1]
    df2 = subprocess.check_output(("udevadm info -a -n %s" % path).split(" "))
    usbid = re.search(device_re, df2).group(1)
    devices[usbid] = path

  return devices


if __name__ == "__main__":
  print "USB Devices:"

  def print_device(uid, path):
    for room in config.OUTPUTS:
      rm = config.OUTPUTS[room]
      for out_id in rm:
        if rm[out_id][1] == uid:
          print "{:14s}{:10s}{:10s}".format(out_id, uid, path)
          return
     
    print "unused      {:10s} {:10s}".format(uid, path)
  

  for (uid, path) in get_connected_usb_devices().items():
    print_device(uid, path)

    
