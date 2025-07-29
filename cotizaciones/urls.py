from django.urls import path
from core import views

app_name = 'cotizaciones'  # Importante para el namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('equipment/create/', views.create_equipment, name='create_equipment'),
    path('quotation/generate/', views.generate_quotation_number, name='generate_quotation_number'),
    path('quotation/search/', views.search_quotation, name='search_quotation'), 
    path('quotation/create/', views.create_complete_quotation, name='create_complete'),
    path('api/validate-format/', views.api_validate_quotation_format, name='api_validate_format'),
]