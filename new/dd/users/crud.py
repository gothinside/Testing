from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from ..models import User, user_role, Role
from ..schemas import UserCreate
from sqlalchemy import select, insert
from ..auth import Hasher
from ..admin import ROLES
from uuid import uuid4

# Исправленная функция получения пользователя по email
async def get_user_by_email(db: AsyncSession, email: str) :
    user = await db.execute(
        select(User).where(User.email == email)
    )
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user

# async def add_new_user_role(db: AsyncSession, user_id: int):
#     await db.commit()

# Исправленная функция создания пользователя
async def create_user(db: AsyncSession, user: UserCreate):
    #if (await get_user_by_email(db, user.email).scalar_one_or_)
    new_user = User(
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True
    )

    # Получение ID роли
    role= await db.execute(
         select(Role).where(Role.role_name == ROLES.ROLE_USER)
     )
    role_id = role.scalars().one_or_none().id
    # Добавление пользователя в БД
    db.add(new_user)
    await db.flush()              
    await db.refresh(new_user)
    await db.execute(
    user_role.insert(), [{"user_id": new_user.id, "role_id": 1}]
        )
    
    # except IntegrityError:
    #     await db.rollback()
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    return new_user
