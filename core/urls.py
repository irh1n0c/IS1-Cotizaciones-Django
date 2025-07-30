from django.urls import path
from core.cotizacion.interfaces.views import (
    crear_cotizacion_form_view,
    crear_cotizacion_view  # 👈 Agrega esta línea
)

from .views import (
    RegistroClienteAPI,
    LoginAPI,
    LogoutAPI,
    home_api,
    dashboard_cliente_api,
    dashboard_admin_api
)

urlpatterns = [
    path('api/registro/', RegistroClienteAPI.as_view(), name='api_registro'),
    path('api/login/', LoginAPI.as_view(), name='api_login'),
    path('api/logout/', LogoutAPI.as_view(), name='api_logout'),
    path('api/home/', home_api, name='api_home'),
    path('api/dashboard/cliente/', dashboard_cliente_api, name='api_dashboard_cliente'),
    path('api/dashboard/admin/', dashboard_admin_api, name='api_dashboard_admin'),
    path('cotizacion/formulario/', crear_cotizacion_form_view, name='cotizacion_formulario'),
    path('cotizacion/crear/', crear_cotizacion_view, name='crear_cotizacion'),
]

