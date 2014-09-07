#!/usr/bin/env python
import os
import sys
import socket
from db_config import DB_FILE_PATH, connect
from db_models import *

yn = None
while yn != 'Y' and yn != 'N':
  yn = raw_input("Delete jarvis configuration and replace with default (Y/N)?")

if yn.upper() != 'Y':
  sys.exit(0)

if os.path.isfile(DB_FILE_PATH):
  print "Removing old db"
  os.remove(DB_FILE_PATH)

print "Creating new db"
(engine, session) = connect(echo=True)

Base.metadata.create_all(engine) 

hostname = socket.gethostname()

session.add_all([
  Path(id="sound", path="Assets/Sounds/"),
  Path(id="holodeck_sound", path="Assets/Holodeck/Sounds/"),
  Path(id="holodeck_images", path="Assets/Holodeck/Images/"),
  Path(id="language_model", path="/home/jarvis/Jarvis/Brain/commands.lm"),
  Path(id="language_dict", path="/home/jarvis/Jarvis/Brain/commands.dic"),

  Room(id="livingroom"),
  Room(id="hackspace"),

  Remote(host="TheMothership", port=9995),
  
  RFModule(
    id="livrm",
    room_id="livingroom", 
    ),
  RFModule(
    id="ctlhs",
    room_id="hackspace", 
  ),
  RFModule(
    id="extra",
    room_id="extra",
  ),
  RFModule(
    id="toddz",
    room_id="todd",
  ),

  USBDevice(
    id="A9MDTZJF", 
    name="RF", 
    controller="RFController", 
    rate=115200,
  ),
  USBDevice(
    id="A602QORA", 
    name="tracklight", 
    controller="RelayController", 
    rate=9600,
  ),
  USBDevice(
    id="A9MX5JNZ", 
    name="windowlight", 
    controller="RGBSingleController", 
    rate=9600,
  ),
  USBDevice(
    id="A70257T7", 
    name="couchlight", 
    controller="RGBSingleController", 
    rate=9600,
  ),
  USBDevice(
    id="A9OZNP19", 
    name="tower", 
    controller="RGBMultiController", 
    rate=115200,
  ),
  USBDevice(
    id="A602KAB4",
    name="runnerlights",
    controller="RunnerLightsController",
    rate=9600,
  ),

  TTSInput(
    id="desk_tts", 
    room_id = "livingroom",
    device="pci-0000:00:1d.7-usb-0:4.7.4:1.0", 
    gain=15,
    host=hostname, 
    port=9000,
  ),
  TTSInput(
    id="livingroom_tts",
    room_id = "livingroom",
    device="pci-0000:00:1d.7-usb-0:4.6:1.0",
    host=hostname,
    gain=30,
    port=9001,
  ),
  TTSInput(
    id="hackspace_tts",
    room_id="hackspace",
    device="pci-0000:00:1d.7-usb-0:4.5:1.0",
    host=hostname,
    gain=15,
    port=9002,
  ),
])

session.commit()

print "Changes commited, new DB initialized."



