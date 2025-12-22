from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.event_repo import EventRepository
from repositories.booking_repo import BookingRepository


class BookingService:
    def __init__(self):
        self.event_repo = EventRepository()
        self.booking_repo = BookingRepository()

    def reserve(self, db: Session, event_id: int, user_id: str):
        event = self.event_repo.get_by_id(db, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event не найден",
            )

        if self.booking_repo.exists_for_user(db, event_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User уже забронировал это место",
            )

        bookings_count = self.booking_repo.count_by_event(db, event_id)
        if bookings_count >= event.total_seats:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Свободных мест нет",
            )

        return self.booking_repo.create(db, event_id, user_id)
