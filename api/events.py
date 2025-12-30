from fastapi.routing import APIRouter
from fastapi import status, Depends, Query
from schemas import EventRequest, EventResponse

from services.event_service import EventService
from core.database import get_db
from sqlalchemy.orm import Session

event_router = APIRouter(prefix="/api/events", tags=["events"])

service = EventService()

@event_router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    request: EventRequest,
    db: Session = Depends(get_db),
    description: str = Query(None, description="Описание события"),
    date: str = Query(None, description="Дата события"),
):
    """Эндпоинт для создания события"""
    event = await service.create_event(
        db=db,
        name=request.name,
        total_seats=request.total_seats,
    )
    return event