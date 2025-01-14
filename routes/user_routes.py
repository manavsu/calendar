from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
import logging
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import bcrypt

from models import get_db, User, Event

log = logging.getLogger(__name__)

router = APIRouter()
    
class UserCreationModel(BaseModel):
    email: str
    password: str


class UserAuthBaseModel(BaseModel):
    email: str
    password: str
    
class EventCreationModel(UserAuthBaseModel):
    start: datetime
    end: datetime
    name: str
    
class EventQueryModel(UserAuthBaseModel):
    start: Optional[datetime] =  None
    end: Optional[datetime] = None
    search_string: Optional[str] = None
    
class EventModel(BaseModel):
    id: int
    start: datetime
    end: datetime
    name: str
    user_id: int
    
    class Config:
        orm_mode = True

def verify_user(email, password, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    
    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return user


@router.post("/user")
async def create_user(user: UserCreationModel, db: Session = Depends(get_db)):
    log.info(f"Creating user {user}")
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    password_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    new_user = User(email=user.email, password_hash=password_hash.decode('utf-8'))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "Success"
    
@router.post("/event")
async def create_event(event: EventCreationModel, db: Session = Depends(get_db)):
    log.info(f"Creating event {event}")
    user = verify_user(event.email, event.password, db)
    
    if event.start > event.end:
        raise HTTPException(status_code=400, detail="Invalid start and end times")
    
    new_event = Event(start=event.start, end=event.end, name=event.name, user_id=user.id)
    
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return "Success"
    
@router.delete("/event/{event_id}")
async def delete_event(event_id: int, user_info:UserAuthBaseModel, db: Session = Depends(get_db)):
    log.info(f"Deleting event {event_id}")
    user = verify_user(user_info.email, user_info.password, db)
    
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event or event.user_id != user.id:
        raise HTTPException(status_code=400, detail="Event not found")
    
    db.delete(event)
    db.commit()
    return "Success"
    
@router.post("/events", response_model=list[EventModel])
async def get_events(query: EventQueryModel, db: Session = Depends(get_db)):
    log.info(f"Getting events for {query.email}")
    
    user = verify_user(query.email, query.password, db)
    events = db.query(Event).filter(Event.user_id == user.id)
    
    if query.start:
        events = events.filter(Event.start >= query.start)
    if query.end:
        events = events.filter(Event.end <= query.end)
    if query.search_string:
        events = events.filter(Event.name.ilike(f"%{query.search_string}%"))
        events = events.filter(Event.notes.ilike(f"%{query.search_string}%"))
    return events.all()
