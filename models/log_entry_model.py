from sqlalchemy import Column, String, Integer
import time

from models import DB_Base

class LogEntry(DB_Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Integer, default=int(time.time()), index=True)
    message = Column(String, nullable=False)

    def __repr__(self):
        return f'<Log Entry id:{self.id} timestamp:{self.timestamp} message:{self.message}>'