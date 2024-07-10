from fastapi import APIRouter, Depends
from . import crud
from ..database import SessionLocal, engine
from sqlalchemy.orm import Session
from ..models import Base
from ..schemas import  CategoryCreate,  CategoryUpdate
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

Base.metadata.create_all(engine)
session = SessionLocal()

@router.get("/")
async def read_items(skip: int = 0, limit: int = 100, session:Session =  Depends(get_db)):
    return crud.get_categories(session, skip, limit)

@router.post("/")
async def new_service(category: CategoryCreate, session:Session =  Depends(get_db)):
    return crud.create_category(session, category)

@router.patch("/{category_id}")
async def patch_category(category_id, 
                         patch_category: CategoryUpdate,
                        session: Session = Depends(get_db)):
    return crud.update_category(session, category_id, patch_category)

@router.delete("/{category_id}")
async def delete_category(category_id, session: Session = Depends(get_db)):
    return crud.delete_category(session, category_id)
