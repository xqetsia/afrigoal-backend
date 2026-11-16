from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserTeam(Base):
    __tablename__ = "user_teams"
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    team_id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)




