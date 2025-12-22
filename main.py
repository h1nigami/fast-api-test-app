from api import booking_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(booking_router)