from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

db_url = "postgresql://postgres:12345678@localhost:5432/fast-api"

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db 
    