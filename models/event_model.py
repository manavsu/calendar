from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from models import DB_Base

class Event(DB_Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    name = Column(String(128), nullable=False)
    notes = Column(String(1024), nullable=True)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="events")

    def __repr__(self):
        return f'<Event id:{self.id} owner_id:{self.owner_id} start:{self.start} end:{self.end}>'