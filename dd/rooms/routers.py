from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas
from ..database import SessionLocal, engine
from ..models import Base
from . import crud
from ..dependies import get_db


router = APIRouter(
    prefix="/rooms",
    tags=["rooms"]
)

Base.metadata.create_all(engine)

@router.get("/")
async def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_rooms(db, skip, limit)

@router.post("/")
async def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db, room)

@router.patch("/{room_num}")
async def update_room(room_num: int, updated_room: schemas.RoomUpdate, db: Session = Depends(get_db)):
    return crud.update_room(db, room_num, updated_room)

@router.delete("/{room_num}")
async def delete_room(room_num: int, db: Session = Depends(get_db)):
    return crud.delete_room(db, room_num)
