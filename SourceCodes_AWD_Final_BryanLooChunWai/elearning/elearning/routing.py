# import libraries and modules
import learnhub.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            learnhub.routing.websocket_urlpatterns
        )
    ),
})
