from fastapi.routing import APIRouter
from fastapi import status, Depends, Query
from schemas import BookingRequest, BookingResponse

from services.booking_service import BookingService
from core.database import get_db
from sqlalchemy.orm import Session


booking_router = APIRouter(prefix="/api/bookings", tags=["bookings"])

service = BookingService()

@booking_router.post("/reserve", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def reserve(
   request: BookingRequest,
   db: Session = Depends(get_db),
   event_id: int = Query(None, description="ID события"),
   user_id: str = Query(None, description="ID пользователя")
                   ):
    """Эндпоинт для бронирования мест"""
    booking = await service.reserve(db=db, event_id=request.event_id, user_id=request.user_id)
    return booking
    