from django.urls import path

from apps.pipline.views import Websocket

websocket_urlpatterns = [
    path('ws', Websocket.as_asgi()),
]
