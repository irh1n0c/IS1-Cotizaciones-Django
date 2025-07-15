from django.urls import path
from .views import RegistroUsuarioView, LoginUsuarioView, perfil_usuario

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('perfil/<str:userid>/', perfil_usuario, name='perfil'),
]