from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from ..repositories.event_repo import EventRepository
from ..repositories.booking_repo import BookingRepository


class BookingService:
    def __init__(self):
        self.event_repo = EventRepository()
        self.booking_repo = BookingRepository()

    async def reserve(self, db: AsyncSession, event_id: int, user_id: str):
        try:
            async with db.begin():
                event = await self.event_repo.get_by_id(db, event_id)
                if not event:
                    raise HTTPException(status.HTTP_404_NOT_FOUND, "Мероприятие не найдено")
                bookings_count = await self.booking_repo.count_by_event(db, event_id)
                if bookings_count >= event[0].total_seats:
                        raise HTTPException(status.HTTP_409_CONFLICT, "Нет свободных мест")
                    
                booking = self.booking_repo.create(db, event_id, user_id)

                return booking
        except IntegrityError:
            raise HTTPException(status.HTTP_409_CONFLICT, "Пользователь уже забронирован")

