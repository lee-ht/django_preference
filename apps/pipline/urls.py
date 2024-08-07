from django.urls import path

from apps.pipline.views import Websocket

urlpatterns = [
    path('ws', Websocket.as_asgi()),
]
