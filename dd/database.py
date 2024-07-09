from sqlalchemy import create_engine, Column, Table, Integer, String, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine(
    "postgresql+psycopg2://postgres:123@localhost/hotel_db",
    echo=True
)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

