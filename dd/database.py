from sqlalchemy import create_engine, Column, Table, Integer, String, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine(
    "postgresql+psycopg2://postgres:123@localhost/myproject",
    echo=True
)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(1000), nullable=False)
    email = Column(String(1000), unique=True, nullable=False)
    phon_number = Column(String(30), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    bookings = relationship("Booking", back_populates="user")

booking_room = Table("booking_room", Base.metadata,
    Column("room_id", Integer, ForeignKey("rooms.room_num"), primary_key=True),
    Column("booking_id", Integer, ForeignKey("bookings.id"), primary_key=True)
)

booking_payment = Table(
    "booking_payment",
    Base.metadata,
    Column("booking_id", Integer, ForeignKey("bookings.id"), primary_key=True),
    Column("payment_id", Integer, ForeignKey("payments.id"), primary_key=True)
)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    join_date = Column(DateTime, nullable=False)
    out_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="bookings")
    rooms = relationship("Room", secondary=booking_room, back_populates="bookings")
    payments = relationship("Payment", secondary=booking_payment, back_populates="bookings")

class Room(Base):
    __tablename__ = "rooms"
    room_num = Column(Integer, nullable=False, primary_key=True)
    room_category = Column(String(50), nullable=False)
    room_price = Column(Integer, nullable=False)
    beds = Column(Integer, default=1, nullable=False)
    is_tv = Column(Boolean, default=True, nullable=False)
    is_wifi = Column(Boolean, default=True, nullable=False)
    bookings = relationship("Booking", secondary=booking_room, back_populates="rooms")

    
class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False)
    payment_date = Column(Date, nullable=False)
    bookings = relationship("Booking", secondary=booking_payment, back_populates="payments")


class Service(Base):
    __tablename__ = "services"
    service_id = Column(Integer, primary_key=True)
    service_name = Column(String(2000), nullable=False)
    service_price = Column(Integer)
    is_active = Column(Boolean, nullable=False, default=True)


#class Employee(Base):
#     __tablename__ = "employees"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#     job_name = Column(String, nullable=False)
#     hire_date = Column(Date, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     salary = Column(Integer, nullable=False)

Base.metadata.create_all(engine)

# Creating a new session
session = SessionLocal()

# Query example
x = session.query(Booking.id, Room.id).join(Booking.rooms).all()
print(x)

# Commit the session (not needed for queries, only for inserts/updates)
session.commit()

# Close the session
session.close()
