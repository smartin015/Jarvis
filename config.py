from Database.db_config import connect
from Database.db_models import *

def _dict_from_query(query, key, val):
  return dict((getattr(row, key), getattr(row, val)) for row in query.all())

(_engine, _session) = connect()

if not _engine or not _session:
  raise Exception("Could not connect to DB!")

RF = _dict_from_query(_session.query(RFModule), 'room_id', 'id')

PATHS = _dict_from_query(_session.query(Path), 'id', 'path')

REMOTES = _session.query(Remote).all()

USB = _session.query(USBDevice).all()

TTS = _session.query(TTSInput).all()

