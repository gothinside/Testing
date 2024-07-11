from fastapi import APIRouter, Depends
from . import crud
from ..database import SessionLocal, engine
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Base
from ..schemas import CategoryCreate, CategoryUpdate

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

# Создаем таблицы в базе данных
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Инициализация таблиц
import asyncio
asyncio.run(init_models())

@router.get("/")
async def read_items(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_db)):
    return await crud.get_categories(session, skip, limit)

@router.post("/")
async def new_service(category: CategoryCreate, session: AsyncSession = Depends(get_db)):
    return await crud.create_category(session, category)

@router.patch("/{category_id}")
async def patch_category(category_id: int, 
                         patch_category: CategoryUpdate,
                         session: AsyncSession = Depends(get_db)):
    return await crud.update_category(session, category_id, patch_category)

@router.delete("/{category_id}")
async def delete_category(category_id: int, session: AsyncSession = Depends(get_db)):
    return await crud.delete_category(session, category_id)
