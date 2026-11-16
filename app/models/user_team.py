from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from app.db import Base

class UserTeam(Base):
    __tablename__ = "user_teams"
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    team_id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)