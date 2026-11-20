from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# FastAPI dependency: opens a session per request and always closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
