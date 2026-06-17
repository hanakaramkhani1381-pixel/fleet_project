def parse_teltonika(hex_data: str):
    try:
        # تبدیل hex به bytes
        data = bytes.fromhex(hex_data)
        
        # پریامبل (4 بایت اول صفر)
        preamble = data[0:4]
        
        # تعداد رکوردها
        record_count = data[9]
        
        # شروع parse رکورد اول
        offset = 10
        
        # timestamp (8 بایت)
        timestamp = int.from_bytes(data[offset:offset+8], 'big')
        offset += 8
        
        # priority (1 بایت)
        offset += 1
        
        # longitude (4 بایت) - تقسیم بر 10000000
        longitude = int.from_bytes(data[offset:offset+4], 'big', signed=True) / 10000000
        offset += 4
        
        # latitude (4 بایت) - تقسیم بر 10000000
        latitude = int.from_bytes(data[offset:offset+4], 'big', signed=True) / 10000000
        offset += 4
        
        # altitude (2 بایت)
        altitude = int.from_bytes(data[offset:offset+2], 'big')
        offset += 2
        
        # angle (2 بایت)
        angle = int.from_bytes(data[offset:offset+2], 'big')
        offset += 2
        
        # satellites (1 بایت)
        satellites = data[offset]
        offset += 1
        
        # speed (2 بایت)
        speed = int.from_bytes(data[offset:offset+2], 'big')
        
        return {
            "timestamp": timestamp,
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude,
            "angle": angle,
            "satellites": satellites,
            "speed": speed
        }
    except Exception as e:
        return {"error": str(e)}


# تست با داده نمونه Teltonika
sample_hex = "000000000000003608010000016B40D8EA30010000016B40D9AD80010000016B40D9C97001000001"
result = parse_teltonika(sample_hex)
print(result)