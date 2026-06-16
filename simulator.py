import requests
import time
import random

# آدرس سرور
BASE_URL = "http://127.0.0.1:8000"

# موقعیت شروع (تهران)
lat = 35.6892
lon = 51.3890

def simulate_vehicle(vehicle_id: int):
    print(f"شبیه‌ساز خودرو {vehicle_id} شروع شد...")
    
    while True:
        # شبیه‌سازی حرکت خودرو
        lat_change = random.uniform(-0.001, 0.001)
        lon_change = random.uniform(-0.001, 0.001)
        
        global lat, lon
        lat += lat_change
        lon += lon_change
        
        speed = random.uniform(20, 120)
        
        # ارسال موقعیت به سرور
        response = requests.post(
            f"{BASE_URL}/location",
            params={
                "vehicle_id": vehicle_id,
                "lat": lat,
                "lon": lon,
                "speed": round(speed, 2)
            }
        )
        
        print(f"خودرو {vehicle_id} | lat: {round(lat,4)} | lon: {round(lon,4)} | speed: {round(speed,1)} km/h")
        
        time.sleep(2)

simulate_vehicle(1)