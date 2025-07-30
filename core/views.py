from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json

# Importar las clases desde tu archivo number_quotation.py
from core.dominio.Servicio_calibracion.number_quotation import (
    QuotationNumberGenerator,
    QuotationFinder
)

from core.dominio.Servicio_calibracion.quotation import (
    EquipmentDetails,
    Quotation
)

def home(request):
    """Vista principal del sistema de cotizaciones"""
    return render(request, 'dashboard.html')

def quotation_home(request):
    """Vista principal del sistema de cotizaciones"""
    return render(request, 'home.html')

def dashboard(request):
    """Dashboard principal con estadísticas"""
    context = {
        'total_cotizaciones': 24,
        'cotizaciones_activas': 8,
        'clientes_activos': 12,
        'equipos_cotizados': 156,
    }
    return render(request, 'dashboard.html', context)

def lista_cotizaciones(request):
    """Lista de cotizaciones con filtros"""
    return render(request, 'lista_cotizaciones.html')


def generate_quotation_number(request):
    """Vista para generar números de cotización"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario HTML
            quotation_type = request.POST.get('type', '').upper().strip()
            sequence_number = int(request.POST.get('sequence', 1))
            
            # Validaciones usando tu clase QuotationNumberGenerator
            if quotation_type not in QuotationNumberGenerator.VALID_TYPES:
                raise ValueError("El tipo debe ser 'C' para Comercial o 'H' para Habitacional")
                
            if not (QuotationNumberGenerator.MIN_SEQUENCE <= sequence_number <= QuotationNumberGenerator.MAX_SEQUENCE):
                raise ValueError(f"Secuencia debe estar entre {QuotationNumberGenerator.MIN_SEQUENCE} y {QuotationNumberGenerator.MAX_SEQUENCE}")
            
            # Generar número usando el formato de tu clase
            year = QuotationNumberGenerator._get_current_year()
            quotation_number = f"{quotation_type}{year}{sequence_number:03d}"
            
            # Renderizar el template con los datos
            return render(request, 'home.html', {
                'quotation_number': quotation_number,
                'type': 'Comercial' if quotation_type == 'C' else 'Habitacional',
                'year': year,
                'sequence': f"{sequence_number:03d}"
            })
            
        except ValueError as e:
            return render(request, 'home.html', {
                'error': str(e)
            })
        except Exception as e:
            return render(request, 'home.html', {
                'error': f'Error inesperado: {str(e)}'
            })
    
    # Si es GET, mostrar el formulario vacío
    return render(request, 'home.html')


def create_equipment(request):
    """Vista para crear equipos médicos"""
    if request.method == 'GET':
        return render(request, 'cotizaciones/create_equipment.html')
    
    elif request.method == 'POST':
        try:
            # Obtener datos del formulario
            name = request.POST.get('name', '').strip()
            brand = request.POST.get('brand', '').strip()
            model = request.POST.get('model', '').strip()
            description = request.POST.get('description', '').strip()
            price = float(request.POST.get('price', 0))
            serial_number = request.POST.get('serial_number', '').strip()
            
            # Crear equipo
            equipment = EquipmentDetails()
            equipment.name = name
            equipment.brand = brand
            equipment.model = model
            equipment.description = description
            equipment.price = price
            equipment.serial_number = serial_number
            
            # Respuesta exitosa
            return JsonResponse({
                'success': True,
                'message': 'Equipo creado exitosamente',
                'equipment': {
                    'name': equipment.name,
                    'brand': equipment.brand,
                    'model': equipment.model,
                    'price': equipment.price,
                    'serial_number': equipment.serial_number
                }
            })
            
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }, status=500)


def search_quotation(request):
    """Vista para buscar cotizaciones"""
    if request.method == 'GET':
        quotation_number = request.GET.get('q', '').strip()
        
        if not quotation_number:
            return render(request, 'cotizaciones/search.html')
        
        try:
            # Simular lista de cotizaciones (aquí conectarías con tu BD)
            mock_quotations = [
                type('MockQuotation', (), {
                    'num_quotation': 'C2025001',
                    'client_name': 'Hospital Central',
                    'date_created': datetime(2025, 1, 15),
                    'equipment_count': 3
                }),
                type('MockQuotation', (), {
                    'num_quotation': 'H2025002',
                    'client_name': 'Clínica Santa María',
                    'date_created': datetime(2025, 1, 20),
                    'equipment_count': 1
                })
            ]
            
            # Buscar cotización usando tu clase QuotationFinder
            found_quotation = QuotationFinder.find_by_number(quotation_number, mock_quotations)
            
            if found_quotation:
                return render(request, 'cotizaciones/search_results.html', {
                    'quotation': found_quotation,
                    'found': True
                })
            else:
                return render(request, 'cotizaciones/search_results.html', {
                    'quotation_number': quotation_number,
                    'found': False
                })
                
        except Exception as e:
            return render(request, 'cotizaciones/search_results.html', {
                'error': str(e),
                'found': False
            })


def create_complete_quotation(request):
    """Vista para crear cotización completa con equipos"""
    if request.method == 'GET':
        return render(request, 'cotizaciones/create_complete.html')
    
    elif request.method == 'POST':
        try:
            # Crear cotización
            quotation = Quotation()
            
            # Datos de cotización
            quotation_type = request.POST.get('quotation_type', 'C')
            sequence = int(request.POST.get('sequence', 1))
            year = datetime.now().year
            quotation.num_quotation = f"{quotation_type}{year}{sequence:03d}"
            quotation.add_current_date()
            
            # Datos de equipo
            equipment = EquipmentDetails()
            equipment.name = request.POST.get('equipment_name')
            equipment.brand = request.POST.get('equipment_brand')
            equipment.model = request.POST.get('equipment_model')
            equipment.description = request.POST.get('equipment_description')
            equipment.price = float(request.POST.get('equipment_price'))
            equipment.serial_number = request.POST.get('equipment_serial')
            
            quotation.add_equipment(equipment)
            
            return render(request, 'cotizaciones/success.html', {
                'quotation': quotation,
                'equipment': equipment
            })
            
        except ValueError as e:
            return render(request, 'cotizaciones/create_complete.html', {
                'error': str(e)
            })
        except Exception as e:
            return render(request, 'cotizaciones/create_complete.html', {
                'error': f'Error inesperado: {str(e)}'
            })


# API Endpoints adicionales
@csrf_exempt
def api_validate_quotation_format(request):
    """API para validar formato de cotización"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quotation_number = data.get('quotation_number', '')
            
            # Usar tu clase para validar el formato
            is_valid = QuotationNumberGenerator.validate_quotation_format(quotation_number)
            
            return JsonResponse({
                'valid': is_valid,
                'quotation_number': quotation_number
            })
            
        except Exception as e:
            return JsonResponse({
                'valid': False,
                'error': str(e)
            }, status=400)