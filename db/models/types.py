from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import Integer, String, DateTime, Boolean    

from db.core.base import Base


class Type(Base):
    __tablename__ = 'types'
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    events = relationship("Event", back_populates="type")