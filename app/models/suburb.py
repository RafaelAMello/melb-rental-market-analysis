from .base import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Suburb(Base):
    __tablename__ = 'suburb'

    name         = Column(String, primary_key=True)
    postcode     = Column(Integer)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, onupdate=datetime.utcnow)
    listings     = relationship("Listing")

    def __init__(self, name, postcode):
        self.name = name
        self.postcode = postcode

    def __repr__(self):
        return f"Suburb({self.name}, {self.postcode})"

    @property
    def slug(self):
        name_slug = '-'.join(self.name.split()).lower()
        return f'{name_slug}-{self.postcode}'
