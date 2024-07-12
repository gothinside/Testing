from fastapi import APIRouter, Depends
from . import crud
from ..database import SessionLocal, engine
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Base
from ..schemas import UserCreate
from ..dependies import get_db

router = APIRouter(
    prefix="/login",
    tags=["users"]
)


@router.post("/")
async def new_service(user: UserCreate, 
                      session: AsyncSession = Depends(get_db)):
    return await crud.create_user(session, user)