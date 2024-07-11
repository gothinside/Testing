from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from .. import models, schemas

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Category).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_category(db: AsyncSession, category: schemas.CategoryCreate):
    existing_category = await db.execute(
        select(models.Category).filter(models.Category.category_name == category.category_name)
    )
    if existing_category.scalars().one_or_none():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Category name must be unique")

    new_category = models.Category(**category.model_dump())

    db.add(new_category)
    
    try:
        await db.commit()
        await db.refresh(new_category)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    return new_category

async def update_category(db: AsyncSession, category_id: int, updated_category: schemas.CategoryUpdate):
    existing_category = await db.execute(
        select(models.Category).filter(models.Category.id == category_id)
    )
    category = existing_category.scalars().one_or_none()
    
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    duplicate_category = await db.execute(
        select(models.Category).filter(models.Category.category_name == updated_category.category_name)
    )
    if duplicate_category.scalars().one_or_none():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Category name must be unique")

    update_data = updated_category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    
    try:
        await db.commit()
        await db.refresh(category)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    return category

async def delete_category(db: AsyncSession, category_id: int):
    existing_category = await db.execute(
        select(models.Category).filter(models.Category.id == category_id)
    )
    category = existing_category.scalars().one_or_none()
    
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    try:
        await db.delete(category)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    return {"message": "Category deleted successfully"}
