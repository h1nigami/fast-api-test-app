from sqlalchemy.ext.asyncio import AsyncSession
from models.event import Event
from sqlalchemy import select

class EventRepository:
    async def get_by_id(self, db: AsyncSession, event_id: int):
        """Асинхронный метод для получения события по ID"""
        query = select(Event).where(Event.id == event_id)
        result = await db.execute(query)
        event = result.first()
        if not event:
            return None
        return event
    
    def create(self, db: AsyncSession, name: str, total_seats: int):
        event = Event(name=name, total_seats=total_seats)
        db.add(event)
        return event
