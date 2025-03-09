from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey    

from db.core.base import Base

from db.models.user_to_event import user_to_event_table


class Event(Base):
    __tablename__ = 'events'
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    date = mapped_column(DateTime, nullable=False)
    is_online = mapped_column(Boolean, nullable=False, default=False)
    organizator_id = mapped_column(ForeignKey)
    user_id = mapped_column(ForeignKey)
    type_id = mapped_column(ForeignKey)
    type = relationship("Type", back_populates="type")
    organizator = relationship("Organizator", back_populates="events")
    users = relationship("User", secondary=user_to_event_table, back_populates="events")