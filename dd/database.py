from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_async_engine(
    "postgresql+asyncpg://postgres:123@localhost/hotel_db",
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=True, class_= AsyncSession)

