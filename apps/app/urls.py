from django.urls import path

from apps.app import views

urlpatterns = [
    # FileResponse
    path('getfile', views.GetFiles.as_view(), name='getfile'),
    # Redis
    path('redis', views.Redis.as_view(), name='index'),
    # Database
    path('save', views.Database.as_view(), name='save'),
    path('get/<str:name>', views.Database.as_view(), name='get'),
    path('delete', views.Database.as_view(), name='delete'),
    # Kafka
    path('kafka', views.Broker.as_view(), name='kafka'),
    # RabbitMQ
    path("rabbit", views.RabbitMQ.as_view(), name='rabbitmq')
]
