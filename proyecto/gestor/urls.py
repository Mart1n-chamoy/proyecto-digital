from django.urls import path
from . import views

urlpatterns = [
    path('', views.saludo, name='saludo'),
    path('inicio/', views.inicio, name='inicio'),
]