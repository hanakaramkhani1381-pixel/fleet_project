from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from auth import hash_password, verify_password, create_token
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from fastapi.middleware.cors import CORSMiddleware
import redis
import json
from teltonika_parser import parse_teltonika

# اتصال به Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# اتصال به دیتابیس - پسورد خودت رو بذار
DATABASE_URL = "postgresql://postgres:13811381@localhost/fleet_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "fleet_secret_key_2024", algorithms=["HS256"])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="توکن معتبر نیست")
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
def get_vehicles(current_user: str = Depends(get_current_user)):
    db = SessionLocal()
    vehicles = db.query(Vehicle).all()
    db.close()
    return vehicles

@app.post("/vehicles")
def add_vehicle(name: str, plate: str, current_user: str = Depends(get_current_user)):
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
def get_location(vehicle_id: int, current_user: str = Depends(get_current_user)):
    # اول توی Redis چک کن
    cached = r.get(f"location:{vehicle_id}")
    if cached:
        return json.loads(cached)
    
    # اگه توی Redis نبود، از دیتابیس بگیر
    db = SessionLocal()
    loc = db.query(Location).filter(Location.vehicle_id == vehicle_id).order_by(Location.id.desc()).first()
    db.close()
    
    if loc:
        data = {
            "vehicle_id": loc.vehicle_id,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "speed": loc.speed,
            "timestamp": str(loc.timestamp)
        }
        # توی Redis ذخیره کن (30 ثانیه)
        r.setex(f"location:{vehicle_id}", 30, json.dumps(data))
        return data
    return {"error": "موقعیتی پیدا نشد"}
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
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(User).filter(User.username == form_data.username).first()
    db.close()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="نام کاربری یا پسورد اشتباه است")
    token = create_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/teltonika/{vehicle_id}")
def receive_teltonika(vehicle_id: int, hex_data: str):
    result = parse_teltonika(hex_data)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    db = SessionLocal()
    loc = Location(
        vehicle_id=vehicle_id,
        latitude=result["latitude"],
        longitude=result["longitude"],
        speed=result["speed"]
    )
    db.add(loc)
    db.commit()
    db.close()
    
    return {"message": "داده Teltonika ذخیره شد", "parsed": result}