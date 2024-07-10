from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException
from ..categories.crud import get_categories
from sqlalchemy.exc import IntegrityError
from fastapi import status
def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()

def create_room(db: Session, room: schemas.RoomCreate):
    if not db.query(models.Category).filter(models.Category.id == room.category_id).one_or_none():
        raise HTTPException(404, "Category not found")
    if db.query(models.Room).filter(models.Room.room_num == room.room_num).one_or_none():
        raise HTTPException(422, "This id is not unique")
    room = models.Room(**room.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def update_room(db: Session, room_num: int, updated_room: schemas.RoomUpdate):
    room = db.query(models.Room).filter(models.Room.room_num == room_num).one_or_none()
    
    if not room:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Room not found")
    if (not db.query(models.Room).filter(models.Room.room_num == updated_room.room_num).one_or_none()) and room_num != updated_room.room_num:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "This id is already exist")
    if not db.query(models.Category).filter(models.Category.id == room.category_id).one_or_none():
        raise HTTPException(404, "Category not found")
    update_data = updated_room.model_dump(exclude_unset=True)
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
