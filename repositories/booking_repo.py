from sqlalchemy.orm import Session
from sqlalchemy import func
from models.booking import Booking


class BookingRepository:
    def count_by_event(self, db: Session, event_id: int) -> int:
        return (
            db.query(func.count(Booking.id))
            .filter(Booking.event_id == event_id)
            .scalar()
        )

    def exists_for_user(self, db: Session, event_id: int, user_id: str) -> bool:
        return (
            db.query(Booking)
            .filter(
                Booking.event_id == event_id,
                Booking.user_id == user_id,
            )
            .first()
            is not None
        )

    def create(self, db: Session, event_id: int, user_id: str) -> Booking:
        booking = Booking(event_id=event_id, user_id=user_id)
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking
