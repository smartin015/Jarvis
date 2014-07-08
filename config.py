
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def _dict_from_query(query, key)
  result = dict((row.key, row) for row in query.all())

(_engine, _session) = connect()

RF = _dict_from_query(_session.query(RFModule))

PATHS = _dict_from_query(_session.query(Path))

OUTPUTS = _dict_from_query(_session.query(USBOutput))

TTS = _dict_from_query(_session.query(TTSInput))

