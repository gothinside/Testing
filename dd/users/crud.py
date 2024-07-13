from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert
from fastapi import HTTPException, status
from ..models import User, user_role, Role
from ..schemas import UserCreate
from ..auth import Hasher
from ..admin import ROLES

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

async def create_user(db: AsyncSession, user: UserCreate):
    new_user = User(
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True
    )

    result = await db.execute(select(Role.id).where(Role.role_name == ROLES.ROLE_USER))
    role_id = result.scalar_one_or_none()

    if role_id is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Role not found")

    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)

        await db.execute(insert(user_role).values(user_id=new_user.id, role_id=role_id))
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    return new_user
