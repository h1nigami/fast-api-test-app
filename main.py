from api import booking_router, event_router
from fastapi import FastAPI
from core.database import Base, engine
from models.booking import Booking
from models.event import Event
import asyncio




app = FastAPI(title="Booking API")

@app.on_event("startup")
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(booking_router)
app.include_router(event_router)