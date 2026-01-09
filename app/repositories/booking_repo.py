from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, exists
from ..models.booking import Booking


class BookingRepository:
    async def count_by_event(self, db: AsyncSession, event_id: int) -> int:
        """Асинхронный подсчет свободных мест"""
        query = select(func.count(Booking.id)).where(Booking.event_id == event_id)
        result = await db.execute(query)
        return result.scalar() or 0

    async def exists_for_user(self, db: AsyncSession, event_id: int, user_id: str) -> bool:
        """Асинхронная проверка существования бронирования"""
        query = select(exists().where(
            (Booking.event_id == event_id) & (Booking.user_id == user_id)
        ))
        result = await db.execute(query)
        return result.scalar()

    def create(self, db: AsyncSession, event_id: int, user_id: str):
        booking = Booking(event_id=event_id, user_id=user_id)
        db.add(booking)
        return booking

