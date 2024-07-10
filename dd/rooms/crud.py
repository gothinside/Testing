from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException

def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()

def create_room(db: Session, room: schemas.RoomCreate):
    room = models.Room(**room.dict())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def update_room(db: Session, room_num: int, updated_room: schemas.RoomUpdate):
    room = db.query(models.Room).filter(models.Room.room_num == room_num).one_or_none()
    
    if not room:
        raise HTTPException(404, "Room not found")
    
    update_data = updated_room.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(room, key, value)
    
    db.commit()
    db.refresh(room)
    return room

def delete_room(db: Session, room_num: int):
    room = db.query(models.Room).filter(models.Room.room_num == room_num).one_or_none()
    
    if not room:
        raise HTTPException(404, "Room not found")
    
    db.delete(room)
    db.commit()
    return {"message": "Room deleted successfully"}
