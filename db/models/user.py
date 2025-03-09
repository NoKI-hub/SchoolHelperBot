from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String

from db.core.base import Base

from db.models.user_to_event import user_to_event_table


class User(Base):
    __tablename__ = 'users'
    
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, nullable=False)
    events = relationship("Events", secondary=user_to_event_table, back_populates="users")