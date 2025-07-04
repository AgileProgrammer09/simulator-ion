import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack  
from iot_dashboard import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iot_dashboard.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  #  Important to keep your normal Django views working
    "websocket": AuthMiddlewareStack(  #  Required to allow user-based WebSocket connections
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
