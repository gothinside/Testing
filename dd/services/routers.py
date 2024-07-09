from fastapi import APIRouter 
from ..crud import get_services, create_service
from . import crud
from ..database import SessionLocal, engine
from ..models import Base
from ..schemas import ServiceCreate,  ServiceUpdate
router = APIRouter(
    prefix="/services",
    tags=["services"]
)

Base.metadata.create_all(engine)
session = SessionLocal()

@router.get("/")
async def read_items(skip: int = 0, limit: int = 100):
    return crud.get_services(session, skip, limit)

@router.post("/")
async def new_service(service: ServiceCreate):
    return crud.create_service(session, service)

@router.patch("/")
async def patch_service(service_id: int, updated_service: ServiceUpdate):
    return crud.update_service(session, service_id, updated_service)

@router.delete("/")
async def delete_service(service_id: int):
    return crud.delete_service(session, service_id)