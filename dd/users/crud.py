from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from ..models import User, user_role, Role
from ..schemas import UserCreate
from sqlalchemy import select, update, insert
from ..auth import Hasher
from ..admin import ROLES
from ..dependies import get_db

async def get_user_by_email(db: AsyncSession, email: str):
    async with db.begin():
        user = await db.execute(
                select(User.email).
                where(User.email == email)
            )
        if not user:
            return HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user

async def create_user(db: AsyncSession, user: UserCreate):
        user = User(
            email =  user.email,
            hashed_password = Hasher.get_password_hash(user.password),
            is_active = True
        )
        role =  await db.execute(
            select(Role.id).
            where(Role.role_name == ROLES.ROLE_USER)
        )
        db.add(user)

        try:
            await db.commit()

            await db.refresh(user)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        
        return user



