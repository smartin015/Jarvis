
DB_FILE_PATH = 'jarvis.db'

def connect(echo=False):
  from sqlalchemy import create_engine
  from sqlalchemy.orm import sessionmaker
  engine = create_engine('sqlite:///%s' % DB_FILE_PATH, echo=echo)
  Session = sessionmaker(bind=engine)
  return (engine, Session())
