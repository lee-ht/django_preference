from django.urls import path
from django.views.generic import TemplateView

from apps.pages import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/index.html')),

    path('index', views.Pages.as_view(), name="index")
]
