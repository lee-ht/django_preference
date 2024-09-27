from django.urls import path, re_path

from apps.pipline.views import Websocket, WebsocketResponse, WebsocketCh

urlpatterns = [
    path('ws', Websocket.as_asgi()),
]

ws_urlpatterns = [
    re_path('ws/ch/(?P<room_name>\w+)/$', WebsocketCh.as_asgi(), name='websocketRQ'),
    re_path('ws/ch1/$', WebsocketResponse.as_asgi(), name='websocketRP')
]
