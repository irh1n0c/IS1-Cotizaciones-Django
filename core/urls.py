from django.urls import path
from .views import (
    RegistroClienteAPI,
    LoginAPI,
    LogoutAPI,
    home_api,
    dashboard_cliente_api,
    dashboard_admin_api
)
from django.views.generic import TemplateView  # ✅ importar TemplateView para renderizar HTML

urlpatterns = [
    path('api/registro/', RegistroClienteAPI.as_view(), name='api_registro'),
    path('api/login/', LoginAPI.as_view(), name='api_login'),
    path('api/logout/', LogoutAPI.as_view(), name='api_logout'),
    path('api/home/', home_api, name='api_home'),
    path('api/dashboard/cliente/', dashboard_cliente_api, name='api_dashboard_cliente'),
    path('api/dashboard/admin/', dashboard_admin_api, name='api_dashboard_admin'),
    path('registro/', TemplateView.as_view(template_name='registro_cliente.html'), name='html_registro'),
    path('login/', TemplateView.as_view(template_name='login.html')),
    path('dashboard-cliente/', TemplateView.as_view(template_name='dashboard_cliente.html')),
    path('', TemplateView.as_view(template_name='home.html'), name='html_home'),
]
