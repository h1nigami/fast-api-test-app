from sqlalchemy.orm import Session
from models.event import Event


class EventRepository:
    def get_by_id(self, db: Session, event_id: int):
        return db.query(Event).filter(Event.id == event_id).first()
    
    def create(self, db: Session, name: str, total_seats: int):
        event = Event(name=name, total_seats=total_seats)
        db.add(event)
        return event
