from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from auth import hash_password, verify_password, create_token
from fastapi.middleware.cors import CORSMiddleware

# اتصال به دیتابیس - پسورد خودت رو بذار
DATABASE_URL = "postgresql://postgres:13811381@localhost/fleet_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# مدل خودرو
class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    plate = Column(String)

# مدل موقعیت GPS
class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

# ساخت جداول
Base.metadata.create_all(engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "سیستم مدیریت ناوگان آنلاین است"}

@app.get("/vehicles")
def get_vehicles():
    db = SessionLocal()
    vehicles = db.query(Vehicle).all()
    db.close()
    return vehicles

@app.post("/vehicles")
def add_vehicle(name: str, plate: str):
    db = SessionLocal()
    v = Vehicle(name=name, plate=plate)
    db.add(v)
    db.commit()
    db.close()
    return {"message": "خودرو اضافه شد"}

@app.post("/location")
def add_location(vehicle_id: int, lat: float, lon: float, speed: float):
    db = SessionLocal()
    loc = Location(vehicle_id=vehicle_id, latitude=lat, longitude=lon, speed=speed)
    db.add(loc)
    db.commit()
    db.close()
    return {"message": "موقعیت ثبت شد"}

@app.get("/location/{vehicle_id}")
def get_location(vehicle_id: int):
    db = SessionLocal()
    loc = db.query(Location).filter(Location.vehicle_id == vehicle_id).order_by(Location.id.desc()).first()
    db.close()
    return loc
@app.post("/register")
def register(username: str, password: str):
    db = SessionLocal()
    hashed = hash_password(password)
    user = User(username=username, password=hashed)
    db.add(user)
    db.commit()
    db.close()
    return {"message": "کاربر ثبت شد"}

@app.post("/login")
def login(username: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if not user or not verify_password(password, user.password):
        return {"error": "نام کاربری یا پسورد اشتباه است"}
    token = create_token({"sub": username})
    return {"token": token}