from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

DB_Base = declarative_base()
engine = create_engine(config.SQLALCHEMY_POSTGRES_DATABASE_URI)
DB_Session_Maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from models.log_entry_model import LogEntry

DB_Base.metadata.create_all(bind=engine)

def get_db():
    db = DB_Session_Maker()
    try:
        yield db
    finally:
        db.close()