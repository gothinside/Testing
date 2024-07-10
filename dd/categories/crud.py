from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException

def get_categories(db: Session, skip: int = 0, limit:int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    category = models.Category(**category.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def update_category(db: Session, category_id:int, updated_category: schemas.CategoryUpdate):
    category = db.query(models.Category).filter(models.Category.id == category_id).one_or_none()
    
    if not category:
        raise HTTPException(404, "Category not found") 

    update_data = updated_category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    
    db.commit()
    db.refresh(category)
    return category

def delete_category(db:Session, category_id:int):
    category = db.query(models.Category).filter(models.Category.id == category_id).one_or_none()
    
    if not category:
        raise HTTPException(404, "Category not found") 
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}