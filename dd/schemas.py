from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date, datetime

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    id: int
    clients: List["Client"] = []

    class Config:
        orm_mode = True

class ClientBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    bookings: List["Booking"] = []
    users: List[User] = []

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    join_date: datetime
    out_date: Optional[datetime] = None

class BookingCreate(BookingBase):
    client_id: int

class Booking(BookingBase):
    id: int
    client: Client
    rooms: List["Room"] = []
    payments: List["Payment"] = []
    services: List["Service"] = []

    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    room_num: int
    category_id: int

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    bookings: List[Booking] = []
    category: "Category"

    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    amount: int
    payment_date: date

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    bookings: List[Booking] = []

    class Config:
        orm_mode = True

class ServiceBase(BaseModel):
    service_name: str
    service_price: Optional[int] = None
    is_active: bool = True

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    service_id: int
    bookings: List[Booking] = []

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    category: str
    price: int
    beds: int = 1
    tables: int = 1
    is_tv: bool = True
    is_wifi: bool = True

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    rooms: List[Room] = []

    class Config:
        orm_mode = True
