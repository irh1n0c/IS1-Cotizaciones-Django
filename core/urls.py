from django.urls import path
from . import views
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

app_name = 'cotizacion'
# URL patterns for the quotations app


urlpatterns = [
    path('api/registro/', RegistroClienteAPI.as_view(), name='api_registro'),
    path('api/login/', LoginAPI.as_view(), name='api_login'),
    path('api/logout/', LogoutAPI.as_view(), name='api_logout'),
    path('api/home/', home_api, name='api_home'),
    path('api/dashboard/cliente/', dashboard_cliente_api, name='api_dashboard_cliente'),
    path('api/dashboard/admin/', dashboard_admin_api, name='api_dashboard_admin'),
    path('cotizacion/formulario/', crear_cotizacion_form_view, name='cotizacion_formulario'),
    path('cotizacion/crear/', crear_cotizacion_view, name='crear_cotizacion'),

    # URLs para equipos médicos josel
    path('medical-equipment/', views.medical_equipment_list, name='medical_equipment_list'),
    path('medical-equipment/create/', views.medical_equipment_create, name='medical_equipment_create'),
    path('medical-equipment/<int:pk>/', views.medical_equipment_detail, name='medical_equipment_detail'),
    path('medical-equipment/<int:pk>/update/', views.medical_equipment_update, name='medical_equipment_update'),
    path('medical-equipment/<int:pk>/delete/', views.medical_equipment_delete, name='medical_equipment_delete'),
]

