from .base import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Listing(Base):
    __tablename__ = 'listing'

    url          = Column(String, primary_key=True, unique=True)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, onupdate=datetime.utcnow)
    suburb_name  = Column(String, ForeignKey('suburb.name'))

    def __init__(self, url, suburb_name):
        self.url = url
        self.suburb_name = suburb_name
