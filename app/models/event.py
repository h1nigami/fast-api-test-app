from sqlalchemy import Column, Integer, String
from ..core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    total_seats = Column(Integer, nullable=False)
