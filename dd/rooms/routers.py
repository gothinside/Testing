from fastapi import APIRouter, Depends
from ..crud import get_services, create_service
from . import crud
from ..database import SessionLocal, engine
from sqlalchemy.orm import Session
from ..models import Base
from ..schemas import  RoomCreate, RoomUpdate
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/rooms",
    tags=["rooms", "categories"]
)

Base.metadata.create_all(engine)
session = SessionLocal()