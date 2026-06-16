# 🚛 سیستم مدیریت ناوگان

یک سیستم بک‌اند کامل برای مدیریت ناوگان خودرویی با قابلیت ردیابی GPS زنده.

## ✅ امکانات
- ثبت و مدیریت خودروها
- دریافت و ذخیره موقعیت GPS بلادرنگ
- سیستم احراز هویت با JWT
- شبیه‌ساز دستگاه GPS (مانند Teltonika)
- نقشه زنده با نمایش موقعیت خودرو
- مستندات کامل API با Swagger

## 🛠 تکنولوژی‌ها
- **زبان:** Python
- **فریم‌ورک:** FastAPI
- **دیتابیس:** PostgreSQL
- **احراز هویت:** JWT
- **نقشه:** Leaflet.js

## 🚀 اجرای پروژه

### ۱. نصب پکیج‌ها
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib

### ۲. اجرای سرور
uvicorn main:app --reload

### ۳. اجرای شبیه‌ساز GPS
python simulator.py

### ۴. مشاهده مستندات API
http://127.0.0.1:8000/docs

### ۵. مشاهده نقشه زنده
فایل map.html را در مرورگر باز کنید.

## 📡 APIها
| Method | URL | کار |
|--------|-----|-----|
| GET | /vehicles | لیست خودروها |
| POST | /vehicles | افزودن خودرو |
| POST | /location | ثبت موقعیت GPS |
| GET | /location/{id} | آخرین موقعیت |
| POST | /register | ثبت‌نام کاربر |
| POST | /login | ورود و دریافت توکن |