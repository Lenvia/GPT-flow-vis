"""
@file: routing.py
@author: Runpu
@time: 2023/5/23 21:51
"""
from django.urls import path, re_path, include
from channels.routing import ProtocolTypeRouter, URLRouter
from server.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/$', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket":
        URLRouter(
            websocket_urlpatterns
        ),
})
