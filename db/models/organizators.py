from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import Integer, String, DateTime, Boolean    

from db.core.base import Base


class Organizator(Base):
    __tablename__ = 'organizators'
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    events = relationship("Events", back_populates="organizator")