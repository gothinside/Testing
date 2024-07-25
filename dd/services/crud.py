from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from .. import models, schemas

async def get_services(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Service).offset(skip).limit(limit))
    return result.scalars().all()

async def create_service(db: AsyncSession, service: schemas.ServiceCreate):
    new_service = models.Service(**service.model_dump())
    db.add(new_service)
    await db.commit()
    await db.refresh(new_service)
    return new_service

async def update_service(db: AsyncSession, service_id: int, updated_service: schemas.ServiceUpdate):
    result = await db.execute(select(models.Service).filter(models.Service.service_id == service_id))
    service = result.scalars().one_or_none()
    
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    update_data = updated_service.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(service, key, value)
    
    await db.commit()
    await db.refresh(service)
    return service

async def delete_service(db: AsyncSession, service_id: int):
    result = await db.execute(select(models.Service).filter(models.Service.service_id == service_id))
    service = result.scalars().one_or_none()
    
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    await db.delete(service)
    await db.commit()
