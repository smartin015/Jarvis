from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Room(Base):
  __tablename__ = 'rooms'
  
  id = Column(String, primary_key=True)

class Path(Base):
  __tablename__ = 'paths'

  id = Column(String, primary_key=True)
  path = Column(String)

class RFModule(Base):
  __tablename__ = 'rf_modules'
  
  RF_ID_LEN = 5
  id = Column(String(RF_ID_LEN), primary_key=True)
  room_id = Column(String)

class USBOutput(Base):
  __tablename__ = 'usb_outputs'

  id = Column(String, primary_key=True)
  name = Column(String)
  controller = Column(String)
  rate = Column(Integer)

class TTSInput(Base):
  __tablename__ = 'tts_servers'

  id = Column(String, primary_key=True)
  room_id = Column(String)
  device = Column(String)
  host = Column(String)
  port = Column(Integer)

if __name__ == "__main__":
  import os
  import sys
  import socket
  from db_config import DB_FILE_PATH, connect

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

    Room(id="livingroom"),
    Room(id="hackspace"),

    RFModule(
      id="livrm",
      room_id="livingroom", 
      ),
    RFModule(
      id="ctlhs",
      room_id="hackspace", 
    ),

    USBOutput(
      id="A9MDTZJF", 
      name="RF", 
      controller="RFController", 
      rate=115200,
    ),
    USBOutput(
      id="A602QORA", 
      name="tracklight", 
      controller="RelayController", 
      rate=9600,
    ),
    USBOutput(
      id="A9MX5JNZ", 
      name="windowlight", 
      controller="RGBSingleController", 
      rate=9600,
    ),
    USBOutput(
      id="A70257T7", 
      name="couchlight", 
      controller="RGBSingleController", 
      rate=9600,
    ),
    USBOutput(
      id="A9OZNP19", 
      name="tower", 
      controller="RGBMultiController", 
      rate=115200,
    ),

    TTSInput(
      id="desk_tts", 
      room_id = "livingroom",
      device="pci-0000:00:1d.7-usb-0:4.7.4:1.0", 
      host=hostname, 
      port=9000,
    ),
    TTSInput(
      id="livingroom_tts",
      room_id = "livingroom",
      device="pci-0000:00:1d.7-usb-0:4.6:1.0",
      host=hostname,
      port=9001,
    ),
    TTSInput(
      id="hackspace_tts",
      room_id="hackspace",
      device="pci-0000:00:1d.7-usb-0:4.5:1.0",
      host=hostname,
      port=9002,
    ),
  ])

  session.commit()

  print "Changes commited, new DB initialized."
  
  

