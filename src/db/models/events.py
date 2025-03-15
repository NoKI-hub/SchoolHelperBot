from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey    

from db.core.base import Base


class Event(Base):
    __tablename__ = 'events'
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    date = mapped_column(DateTime, nullable=False)
    participant = mapped_column(String, nullable=False)
    is_online = mapped_column(Boolean, nullable=False, default=False)
    organizator = mapped_column(String, nullable=False)
    type = mapped_column(String, nullable=False)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="events")