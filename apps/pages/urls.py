from django.urls import path

from apps.pages import views

urlpatterns = [
    path('index', views.Pages.as_view(), name="index")
]
