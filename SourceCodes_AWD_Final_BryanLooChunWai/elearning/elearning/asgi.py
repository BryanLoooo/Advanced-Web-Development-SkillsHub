# import libraries and modules
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elearning.settings")

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from learnhub.routing import websocket_urlpatterns

# define application for ASGI file
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
