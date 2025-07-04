import requests
import random
from datetime import datetime, timezone
import time

#  API endpoint to send sensor data
API_URL = "http://localhost:8000/api/sensor-data/"

#  JWT access token (required for authentication)
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNTMxNDEwLCJpYXQiOjE3NTE1MzExMTAsImp0aSI6IjNiNzBmNDY4NGJmYTQwM2FhNzdhOGZmYzBjYjEyZWQ5IiwidXNlcl9pZCI6MX0.ZQ_xEh4soLguhU8LWVWoZ_mYH5veY7C-cxehWSi-TLQ"

#  Loop continuously to simulate temperature sensor readings
while True:
    #  Generate fake sensor data
    data = {
        "sensor_id": "sensor_1",  # ID of the sensor
        "temperature": round(random.uniform(20.0, 60.0), 2),  # Random temperature value
        "timestamp": datetime.now(timezone.utc).isoformat()  # Current time in ISO format
    }

    #  Set headers with JWT token
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Content-Type": "application/json"
    }

    #  Try to send data to the API
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        print("Sent:", data, "Status:", response.status_code)
    except Exception as e:
        print("Error sending data:", e)

    #  Wait for 5 seconds before sending next reading
    time.sleep(5)
