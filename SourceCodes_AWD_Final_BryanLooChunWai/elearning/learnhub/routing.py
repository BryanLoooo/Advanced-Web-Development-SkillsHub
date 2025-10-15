# import libraries and modules
from django.urls import re_path
from . import consumers

# set up websocket url patterns
websocket_urlpatterns = [
    re_path(r"^ws/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
