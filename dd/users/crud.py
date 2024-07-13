from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from ..models import User, user_role, Role
from ..schemas import UserCreate
from sqlalchemy import select, insert
from ..auth import Hasher
from ..admin import ROLES

# Исправленная функция получения пользователя по email
async def get_user_by_email(db: AsyncSession, email: str):
    async with db.begin():
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()  # scalar_one_or_none() вернёт None, если пользователь не найден
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user

# Исправленная функция создания пользователя
async def create_user(db: AsyncSession, user: UserCreate):
    new_user = User(
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True
    )

    # Получение ID роли
    result = await db.execute(
        select(Role.id).where(Role.role_name == ROLES.ROLE_USER)
    )
    role_id = result.scalar_one_or_none()

    if role_id is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Role not found")

    # Добавление пользователя в БД
    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)

        # Связывание пользователя с ролью
        await db.execute(
            insert(user_role).values(user_id=new_user.id, role_id=role_id)
        )
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    return new_user
