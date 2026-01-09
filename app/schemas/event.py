from pydantic import BaseModel, Field


class EventResponse(BaseModel):
    id: int
    name: str
    total_seats: int = Field(..., ge=0)

    class Config:
        from_attributes = True

class EventRequest(BaseModel):
    name: str = Field(..., min_length=1)
    total_seats: int = Field(..., gt=0)