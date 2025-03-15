from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String

from db.core.base import Base


class User(Base):
    __tablename__ = 'users'
    
    id = mapped_column(Integer, primary_key=True)
    fullname = mapped_column(String, nullable=False)
    events = relationship("Event", back_populates="user")