from pydantic import BaseModel
from datetime import date, datetime

class Users(BaseModel):
    id:int
    username:str
    hased_password:str
    email:str
    phone:str
    is_active:bool

class Booking(BaseModel):
    id:int|None
    join_date: datetime
    out_date : None | datetime
    user_id: int

class Room(BaseModel):
    id:int|None
    room_num: int|None
    room_cat: str|None
    room_price: int|None

class Payment(BaseModel):
    id:int
    amount: int
    payment_date: datetime
    
