from sqlalchemy.orm import Session
from .. import models, schemas
from passlib.context import CryptContext
from fastapi import HTTPException

def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Service).offset(skip).limit(limit).all()

def create_service(db: Session, service: schemas.ServiceCreate):
    service = models.Service(**service.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

def update_service(db: Session, service_id:int, updated_service: schemas.ServiceUpdate):
    service = db.query(models.Service).filter(models.Service.service_id == service_id).one_or_none()
    
    if not service:
        raise HTTPException(404, "Service not found") 

    update_data = updated_service.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(service, key, value)
    
    db.commit()
    db.refresh(service)
    return service

def delete_service(db:Session, service_id):
    service = db.query(models.Service).filter(models.Service.service_id == service_id).one_or_none()
    
    if not service:
        raise HTTPException(404, "Service not found") # or raise an appropriate exception
    
    db.delete(service)
    db.commit()
