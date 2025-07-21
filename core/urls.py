from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro_cliente, name='registro_cliente'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard_cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
]
