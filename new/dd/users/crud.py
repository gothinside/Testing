from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from ..models import User, user_role, Role
from ..schemas import UserCreate
from sqlalchemy import select, insert
from ..auth import Hasher
from ..admin import ROLES
from uuid import uuid4

# Function to get a user by email
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalars().one_or_none()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user

# Function to create a new user
async def create_user(db: AsyncSession, user: UserCreate):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already exists")
    
    new_user = User(
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True
    )

    # Add new user to the session and commit to get the user ID
    db.add(new_user)
    await db.commit()              
    await db.refresh(new_user)

    # Get the ID of the role
    result = await db.execute(
        select(Role).where(Role.role_name == ROLES.ROLE_USER)
    )
    role = result.scalars().one_or_none()
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Role not found")
    
    role_id = role.id

    # Insert the user role into user_role table
    await db.execute(
        user_role.insert().values(user_id=new_user.id, role_id=role_id)
    )
    
    await db.commit()  # Commit the transaction

    return new_user
