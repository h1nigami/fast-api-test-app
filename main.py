from api import booking_router
from fastapi import FastAPI
from core.database import Base, engine
from models.booking import Booking
from models.event import Event

Base.metadata.create_all(engine)

app = FastAPI(title="Booking API")

app.include_router(booking_router)