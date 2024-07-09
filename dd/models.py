from sqlalchemy import Column, Table, Integer, String, Date, Boolean, ForeignKey, DateTime
from .database import Base
from sqlalchemy.orm import relationship

client_user = Table(
    "client_user",
    Base.metadata,
    Column("client_id", Integer, ForeignKey("clients.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
)

booking_room = Table(
    "booking_room",
    Base.metadata,
    Column("room_num", Integer, ForeignKey("rooms.room_num"), primary_key=True),
    Column("booking_id", Integer, ForeignKey("bookings.id"), primary_key=True)
)

booking_payment = Table(
    "booking_payment",
    Base.metadata,
    Column("booking_id", Integer, ForeignKey("bookings.id"), primary_key=True),
    Column("payment_id", Integer, ForeignKey("payments.id"), primary_key=True)
)

booking_service = Table(
    "booking_service",
    Base.metadata,
    Column("booking_id", Integer, ForeignKey("bookings.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("services.service_id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(1000), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    clients = relationship("Client", secondary=client_user, back_populates="users")

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=True, index=True)
    bookings = relationship("Booking", back_populates="client")
    users = relationship("User", secondary=client_user, back_populates="clients")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    join_date = Column(DateTime, nullable=False)
    out_date = Column(DateTime, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="bookings")
    rooms = relationship("Room", secondary=booking_room, back_populates="bookings")
    payments = relationship("Payment", secondary=booking_payment, back_populates="bookings")
    services = relationship("Service", secondary=booking_service, back_populates="bookings")

class Room(Base):
    __tablename__ = "rooms"
    room_num = Column(Integer, nullable=False, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    bookings = relationship("Booking", secondary=booking_room, back_populates="rooms")
    category = relationship("Category", back_populates="rooms")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    bookings = relationship("Booking", secondary=booking_payment, back_populates="payments")

class Service(Base):
    __tablename__ = "services"
    service_id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(255), nullable=False, index = True)
    service_price = Column(Integer)
    is_active = Column(Boolean, nullable=False, default=True)
    bookings = relationship("Booking", secondary=booking_service, back_populates="services")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(255), unique=True, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    beds = Column(Integer, default=1, nullable=False)
    tables = Column(Integer, default=1, nullable=False)
    is_tv = Column(Boolean, default=True, nullable=False)
    is_wifi = Column(Boolean, default=True, nullable=False)
    rooms = relationship("Room", back_populates="category")
