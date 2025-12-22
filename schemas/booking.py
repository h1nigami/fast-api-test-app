import datetime
from pydantic import Field, BaseModel

class BookingRequest(BaseModel):
    event_id: int = Field(..., gt=0)
    user_id: str = Field(..., min_length=1)

class BookingResponse(BaseModel):
    id:int
    event_id:int
    user_id:str
    created_at:datetime.datetime

    class Config:
        from_attributes = True