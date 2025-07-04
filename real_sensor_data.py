import requests
from datetime import datetime, timezone
import time

# OpenWeatherMap API key 
WEATHER_API = "https://api.openweathermap.org/data/2.5/weather?q=indore&appid=916c8f6bb9bd4cb0d2926d1a0dd2237b&units=metric"

# Django REST API endpoint where sensor data will be sent
DJANGO_API = "http://127.0.0.1:8000/api/sensor-data/"
# JWT token for API authentication 
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNTUzODY2LCJpYXQiOjE3NTE1NTM1NjYsImp0aSI6ImFiM2ViNTkzZmE3YjQ4M2I5YjA2MTM3YzY2NzBlMjEwIiwidXNlcl9pZCI6MX0.5kMtq0SdKLS8pfdQHDTRMkeulndRgSeJ7pMXtHFx7RA"

# Continuously run the script
while True:
    try:
        # Get current temperature from weather API
        response = requests.get(WEATHER_API)
        data = response.json()

        # Check if the response contains temperature data
        if 'main' in data:
            temperature = data['main']['temp']
            print(type(temperature))
            #  Get current timestamp in UTC format
            timestamp = datetime.now(timezone.utc).isoformat()

            # Prepare data to send to Django backend
            payload = {
                "sensor_id": "real_sensor_1",  # Custom sensor ID
                "temperature" : data['main']['temp'],  
                "timestamp": timestamp
            }

            # Set headers with JWT token and content type
            headers = {
                "Authorization": f"Bearer {JWT_TOKEN}",
                "Content-Type": "application/json"
            }

            # Send temperature data to Django API
            res = requests.post(DJANGO_API, json=payload, headers=headers)
            print("Sent:", payload, "| Status:", res.status_code)
        else:
            # Print API error if temperature info is missing
            print("API Error:", data)

    except Exception as e:
        # Catch and print any unexpected errors
        print("Error:", e)

    # Wait 10 sec before next reading
    time.sleep(10)
