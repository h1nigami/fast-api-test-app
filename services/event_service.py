from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.event_repo import EventRepository
from sqlalchemy.exc import IntegrityError


class EventService:
    def __init__(self):
        self.event_repo = EventRepository()

    async def create_event(self, db: AsyncSession, name: str, total_seats: int):
        try:
            async with db.begin():
                event = self.event_repo.create(db, name, total_seats)
                return event
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event with this name already exists",
            )