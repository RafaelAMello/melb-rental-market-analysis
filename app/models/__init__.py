from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from .base import Base
from .suburb import Suburb
from .listing import Listing

from app import config

ENGINE = create_engine(URL(**config.DATABASE_CREDENTIALS), echo=True)
Base.metadata.create_all(bind=ENGINE)
Session = sessionmaker(bind=ENGINE)
