from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumer import AdConsumer

websockets = URLRouter([
    re_path(r".*", AdConsumer.as_asgi(), name="ad_get_info",),
])