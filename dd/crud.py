from sqlalchemy.orm import Session
import models, schemas 
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hashed_algorithm(password: str):
    return pwd_context.hash(password)

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    if(user):
        db.delete(user)
        db.commit()
    return user

def create_user(db: Session, user: schemas.UserCreate):
    user.password = hashed_algorithm(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, user_id: int):
    q = db.query(models.User.username).filter(models.User.id == user_id).one_or_none()
    return q
