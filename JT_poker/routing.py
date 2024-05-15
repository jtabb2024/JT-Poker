# your_app/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/playPoker/$', consumers.PokerConsumer.as_asgi()),
]
