from fastapi.routing import APIRouter
from schemas import BookingRequest, BookingResponse
booking_router = APIRouter(prefix="/api/bookings")

@booking_router.post("/reserve", response_model=BookingResponse)
def reserve(request: BookingRequest):
    pass