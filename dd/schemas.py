from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date, datetime

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    is_active: Optional[bool]
    hashed_password: Optional[str]

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

class ClientUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]

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

class BookingUpdate(BaseModel):
    join_date: Optional[datetime]
    out_date: Optional[datetime]
    client_id: Optional[int]

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

class RoomUpdate(BaseModel):
    room_num: Optional[int]
    category_id: Optional[int]

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

class PaymentUpdate(BaseModel):
    amount: Optional[int]
    payment_date: Optional[date]

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

class ServiceUpdate(BaseModel):
    service_name: Optional[str]
    service_price: Optional[int]
    is_active: Optional[bool]

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

class CategoryUpdate(BaseModel):
    category: Optional[str]
    price: Optional[int]
    beds: Optional[int]
    tables: Optional[int]
    is_tv: Optional[bool]
    is_wifi: Optional[bool]

class Category(CategoryBase):
    id: int
    rooms: List[Room] = []

    class Config:
        orm_mode = True
