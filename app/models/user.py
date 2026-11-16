from sqlalchemy import Column, String, DateTime
from datetime import datetime

from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)