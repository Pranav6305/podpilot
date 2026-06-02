from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# engine is the component that knows how to talk with postgreSQL


def get_db():
    db = SessionLocal() # creates session
    try:
        yield db # FastAPI will receive the session and runs the route
    finally: # helps to prevent exhaustion without raising an exception
        db.close() # session is cleaned up
