from api import booking_router
from fastapi import FastAPI

app = FastAPI(title="Booking API")

app.include_router(booking_router)