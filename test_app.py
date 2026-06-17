from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# تست ۱: سرور آنلاینه؟
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "سیستم مدیریت ناوگان آنلاین است"}
    print("✅ تست ۱ پاس شد: سرور آنلاینه")

# تست ۲: بدون توکن دسترسی نداری؟
def test_no_token():
    response = client.get("/vehicles")
    assert response.status_code == 401
    print("✅ تست ۲ پاس شد: بدون توکن دسترسی نیست")

# تست ۳: ثبت‌نام کاربر جدید
def test_register():
    response = client.post("/register?username=testuser&password=test123")
    assert response.status_code == 200
    print("✅ تست ۳ پاس شد: ثبت‌نام کار می‌کنه")

# تست ۴: لاگین
def test_login():
    response = client.post("/login", data={"username": "testuser", "password": "test123"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    print("✅ تست ۴ پاس شد: لاگین کار می‌کنه")

# تست ۵: parser Teltonika
def test_teltonika_parser():
    from teltonika_parser import parse_teltonika
    result = parse_teltonika("000000000000003608010000016B40D8EA30010000016B40D9AD80010000016B40D9C97001000001")
    assert "latitude" in result
    assert "longitude" in result
    assert "speed" in result
    print("✅ تست ۵ پاس شد: Teltonika parser کار می‌کنه")

# اجرای همه تست‌ها
if __name__ == "__main__":
    test_home()
    test_no_token()
    test_register()
    test_login()
    test_teltonika_parser()
    print("\n🎉 همه تست‌ها پاس شدن!")