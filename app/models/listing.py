from .base import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Listing(Base):
    __tablename__ = 'listing'

    url        = Column(String, primary_key=True, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    def __init__(self, url):
        self.url = url
