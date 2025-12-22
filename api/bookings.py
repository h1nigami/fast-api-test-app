from fastapi.routing import APIRouter
from fastapi import status
from schemas import BookingRequest, BookingResponse


booking_router = APIRouter(prefix="/api/bookings", tags=["bookings"])

@booking_router.post("/reserve", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def reserve(request: BookingRequest):
    """Временная заглушка"""
    return BookingResponse(
        id=1,
        event_id=request.event_id,
        user_id=request.user_id,
    )