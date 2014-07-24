from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Room(Base):
  __tablename__ = 'rooms'
  
  id = Column(String, primary_key=True)

class Remote(Base):
  __tablename__ = 'remotes'
  
  host = Column(String, primary_key=True)
  port = Column(Integer)  
  
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

