import re
import subprocess

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
  from config import USB
  print "USB Devices:"
  fmt = "{:14s}{:10s}{:10s}"
  print fmt.format("NAME", "USB_ID", "PATH")
  def print_device(uid, path):
    for o in USB:
      if o.id == uid:
        print fmt.format(o.name, uid, path)
        return
     
    print fmt.format("unused", uid, path)
  

  for (uid, path) in get_connected_usb_devices().items():
    print_device(uid, path)

    
