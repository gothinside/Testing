from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas
from sqlalchemy.exc import IntegrityError
async def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    async with db.begin():
        return await db.query(models.Room).offset(skip).limit(limit).all()

def create_room(db: Session, room: schemas.RoomCreate):
    if not db.query(models.Category).filter(models.Category.id == room.category_id).one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    if db.query(models.Room).filter(models.Room.room_num == room.room_num).one_or_none():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="This room number is not unique")
    
    new_room = models.Room(**room.model_dump())
    
    try:
        db.add(new_room)
        db.commit()
        db.refresh(new_room)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    return new_room

def update_room(db: Session, room_num: int, updated_room: schemas.RoomUpdate):
    room = db.query(models.Room).filter(models.Room.room_num == room_num).one_or_none()
    
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    
    if not db.query(models.Category).filter(models.Category.id == updated_room.category_id).one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    if (not db.query(models.Room).filter(models.Room.room_num == updated_room.room_num).one_or_none()) and room_num != updated_room.room_num:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This room number already exists")
    
    
    update_data = updated_room.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(room, key, value)
    
    try:
        db.commit()
        db.refresh(room)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    return room

def delete_room(db: Session, room_num: int):
    room = db.query(models.Room).filter(models.Room.room_num == room_num).one_or_none()
    
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    
    try:
        db.delete(room)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    return {"message": "Room deleted successfully"}
