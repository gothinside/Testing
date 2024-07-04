from sqlalchemy import create_engine
from sqlalchemy import Column,Table, Integer, String, Date, Boolean,ForeignKey,DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy import update, text, Null, insert

engine = create_engine(
    "postgresql+psycopg2://postgres:123@localhost/myproject",
    echo=True
)
base = declarative_base()
Session = Session(bind = engine)


class User(base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    smth = Column(Integer)
    children = relationship("Booking", back_populates="parent")

booking_room = Table("booking_room", base.metadata,
                    Column("room_id", Integer(), ForeignKey("rooms.id")),
                    Column("booking_id", Integer(), ForeignKey("bookings.id"))
                    )

booking_oplata = Table(
    "booking_oplata",
    base.metadata,
    Column("booking_id", Integer(), ForeignKey("booking.id")),
    Column("oplata_id", Integer(), ForeignKey("oplata.id"))
)

class Booking(base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True,autoincrement=True)
    join_date = Column(DateTime, nullable=False)
    out_date = Column(DateTime)
    owner = Column(Integer, ForeignKey("Users.id"))
    parent = relationship("User", back_populates="children")
    relationship("Room", secondary=booking_room, back_populates="parents")
    relationship("Oplata", secondary=booking_oplata)


class Room(base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_num = Column(Integer)
    relationship("Booking", secondary=booking_room, back_populates="children")


class Oplata(base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    summa = Column(Integer)
    oplata_date = Column(Date)

class Sotrudnic(base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    job_name = Column(String)
    hire_date = Column(Date)
    email = Column(String)
    salary = Column(Integer)

base.metadata.create_all(engine)
x = Session.query(Booking.id, Room.id).join(Room).all()
print(x)

Session.commit()