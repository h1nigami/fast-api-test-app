from pydantic import BaseModel, Field, ConfigDict


class EventResponse(BaseModel):
    id: int
    name: str
    total_seats: int = Field(..., ge=0)

    model_config = ConfigDict(from_attributes = True)

class EventRequest(BaseModel):
    name: str = Field(..., min_length=1)
    total_seats: int = Field(..., gt=0)