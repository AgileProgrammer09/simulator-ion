from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SensorDataConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        # When client connects, join the 'sensor_data' group
        group = "sensor_data"
        await self.channel_layer.group_add(group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # When client disconnects, leave the group
        await self.channel_layer.group_discard("sensor_data", self.channel_name)

    async def receive(self, text_data):
        # Not used for now (client doesn't send anything)
        pass

    async def send_sensor_data(self, event):
        # Send the sensor data (received from backend) to frontend via WebSocket
        sensor_data = event["data"]
        await self.send(text_data=json.dumps(sensor_data))
