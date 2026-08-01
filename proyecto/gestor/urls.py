from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('documentos/', views.documentos, name='documentos'),
    path('documentos/crear/', views.crear_documento, name='crear'),
    path('documentos/editar/', views.editar_documento, name='editar'),
]