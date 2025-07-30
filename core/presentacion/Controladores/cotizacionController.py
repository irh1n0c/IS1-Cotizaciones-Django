#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List, Optional, Dict, Any
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

from core.dominio.Servicio_calibracion.quotation import Quotation, EquipmentDetails
from core.dominio.Servicio_calibracion.cotizacionID import CotizacionID
from core.dominio.Servicio_calibracion.estadoCotizacion import EstadoCotizacion, TipoUsuario
from core.dominio.Servicio_calibracion.usuario import Usuario
from core.servicios.cotizacionServicioImpl import CotizacionServicioImpl
from core.servicios.repositories import RepositoryFactory
from core.dominio.Servicio_calibracion.domain_events import get_domain_event_dispatcher


class CotizacionController(View):
    """Controlador para operaciones de cotizaciones con arquitectura DDD."""
    
    def __init__(self):
        super().__init__()
        # Inicializar repositorios y servicios
        self._repository_factory = RepositoryFactory()
        self._domain_event_dispatcher = get_domain_event_dispatcher()
    
    def _get_current_user(self, request: HttpRequest) -> Optional[Usuario]:
        """Obtiene el usuario actual de la sesión."""
        # Aquí implementarías la lógica para obtener el usuario de la sesión
        # Por ahora retornamos None, pero debería integrarse con el sistema de auth
        user_id = request.session.get('user_id')
        if user_id:
            user_repo = self._repository_factory.create_usuario_repository(None)
            return user_repo.find_by_id(user_id)
        return None
    
    def _validate_user_permissions(self, user: Usuario, action: str) -> bool:
        """Valida permisos del usuario para una acción específica."""
        if not user or not user.is_active:
            return False
        
        permission_map = {
            'create': user.puede_crear_cotizacion(),
            'update': user.puede_modificar_cotizacion(),
            'delete': user.puede_eliminar_cotizacion(),
            'read': True  # Todos pueden leer (con restricciones por contexto)
        }
        
        return permission_map.get(action, False)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request: HttpRequest) -> JsonResponse:
        """Crea una nueva cotización."""
        try:
            # Obtener usuario actual
            user = self._get_current_user(request)
            if not self._validate_user_permissions(user, 'create'):
                return JsonResponse({
                    'success': False,
                    'error': 'No tiene permisos para crear cotizaciones'
                }, status=403)
            
            # Parsear datos
            data = json.loads(request.body)
            cliente_id = data.get('cliente_id')
            equipos_data = data.get('equipos', [])
            
            if not cliente_id:
                return JsonResponse({
                    'success': False,
                    'error': 'cliente_id es requerido'
                }, status=400)
            
            # Crear equipos
            equipos = []
            for equipo_data in equipos_data:
                equipo = EquipmentDetails()
                equipo.name = equipo_data.get('name')
                equipo.brand = equipo_data.get('brand')
                equipo.model = equipo_data.get('model')
                equipo.description = equipo_data.get('description', '')
                equipo.price = float(equipo_data.get('price', 0))
                equipo.serial_number = equipo_data.get('serial_number')
                equipos.append(equipo)
            
            # Crear servicio con repositorios apropiados
            cotizacion_repo = self._repository_factory.create_cotizacion_repository(
                user.tipo_usuario, None
            )
            cliente_repo = self._repository_factory.create_cliente_repository(None)
            
            cotizacion_service = CotizacionServicioImpl(
                cotizacion_repo, cliente_repo, None
            )
            
            # Crear cotización
            cotizacion = cotizacion_service.crear_cotizacion_dinamica(
                user.user_id, cliente_id, equipos, user
            )
            
            # Procesar domain events
            for event in cotizacion.get_domain_events():
                self._domain_event_dispatcher.dispatch(event)
            cotizacion.clear_domain_events()
            
            return JsonResponse({
                'success': True,
                'data': {
                    'cotizacion_id': str(cotizacion.cotizacion_id),
                    'numero_cotizacion': cotizacion.numero_cotizacion,
                    'estado': cotizacion.estado.value,
                    'total': str(cotizacion.total)
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
                'error': f'Error interno: {str(e)}'
            }, status=500)
    
    def get(self, request: HttpRequest, cotizacion_id: str = None) -> JsonResponse:
        """Obtiene una o varias cotizaciones."""
        try:
            # Obtener usuario actual
            user = self._get_current_user(request)
            if not self._validate_user_permissions(user, 'read'):
                return JsonResponse({
                    'success': False,
                    'error': 'No tiene permisos para leer cotizaciones'
                }, status=403)
            
            # Crear repositorio apropiado según el tipo de usuario
            cotizacion_repo = self._repository_factory.create_cotizacion_repository(
                user.tipo_usuario, None
            )
            
            if cotizacion_id:
                # Obtener cotización específica
                cotizacion = cotizacion_repo.find_by_id(CotizacionID.from_string(cotizacion_id))
                
                if not cotizacion:
                    return JsonResponse({
                        'success': False,
                        'error': 'Cotización no encontrada'
                    }, status=404)
                
                # Validar permisos específicos
                if user.es_cliente() and not cotizacion.es_visible_para_cliente(user.user_id):
                    return JsonResponse({
                        'success': False,
                        'error': 'No tiene permisos para ver esta cotización'
                    }, status=403)
                
                # Marcar como vista si es cliente
                if user.es_cliente():
                    cotizacion.marcar_como_vista_por_cliente()
                    cotizacion_repo.save(cotizacion)
                
                return JsonResponse({
                    'success': True,
                    'data': self._serialize_cotizacion(cotizacion)
                })
            
            else:
                # Obtener lista de cotizaciones
                if user.es_empresa():
                    cotizaciones = cotizacion_repo.find_by_empresa(user.user_id)
                else:
                    cotizaciones = cotizacion_repo.find_by_cliente(user.user_id)
                
                return JsonResponse({
                    'success': True,
                    'data': [self._serialize_cotizacion(c) for c in cotizaciones]
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=500)
    
    def put(self, request: HttpRequest, cotizacion_id: str) -> JsonResponse:
        """Actualiza una cotización."""
        try:
            # Obtener usuario actual
            user = self._get_current_user(request)
            if not self._validate_user_permissions(user, 'update'):
                return JsonResponse({
                    'success': False,
                    'error': 'No tiene permisos para actualizar cotizaciones'
                }, status=403)
            
            # Obtener cotización
            cotizacion_repo = self._repository_factory.create_cotizacion_repository(
                user.tipo_usuario, None
            )
            cotizacion = cotizacion_repo.find_by_id(CotizacionID.from_string(cotizacion_id))
            
            if not cotizacion:
                return JsonResponse({
                    'success': False,
                    'error': 'Cotización no encontrada'
                }, status=404)
            
            # Parsear datos
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'enviar':
                cotizacion.enviar_cotizacion(user.user_id, user.tipo_usuario)
            
            elif action == 'aprobar' and user.es_cliente():
                cotizacion.aprobar()
            
            elif action == 'rechazar' and user.es_cliente():
                motivo = data.get('motivo', '')
                cotizacion.rechazar(motivo)
            
            elif action == 'cancelar' and user.es_empresa():
                motivo = data.get('motivo', '')
                cotizacion.cancelar(user.user_id, user.tipo_usuario, motivo)
            
            elif action == 'agregar_equipo' and user.es_empresa():
                equipo_data = data.get('equipo')
                equipo = EquipmentDetails()
                equipo.name = equipo_data.get('name')
                equipo.brand = equipo_data.get('brand')
                equipo.model = equipo_data.get('model')
                equipo.description = equipo_data.get('description', '')
                equipo.price = float(equipo_data.get('price', 0))
                equipo.serial_number = equipo_data.get('serial_number')
                
                cotizacion.agregar_equipo(equipo, user.user_id, user.tipo_usuario)
            
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Acción no válida o no permitida'
                }, status=400)
            
            # Guardar cambios
            cotizacion_repo.save(cotizacion)
            
            # Procesar domain events
            for event in cotizacion.get_domain_events():
                self._domain_event_dispatcher.dispatch(event)
            cotizacion.clear_domain_events()
            
            return JsonResponse({
                'success': True,
                'data': self._serialize_cotizacion(cotizacion)
            })
            
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=500)
    
    def delete(self, request: HttpRequest, cotizacion_id: str) -> JsonResponse:
        """Elimina una cotización."""
        try:
            # Obtener usuario actual
            user = self._get_current_user(request)
            if not self._validate_user_permissions(user, 'delete'):
                return JsonResponse({
                    'success': False,
                    'error': 'No tiene permisos para eliminar cotizaciones'
                }, status=403)
            
            # Solo empresas pueden eliminar
            if not user.es_empresa():
                return JsonResponse({
                    'success': False,
                    'error': 'Solo las empresas pueden eliminar cotizaciones'
                }, status=403)
            
            # Obtener cotización
            cotizacion_repo = self._repository_factory.create_cotizacion_repository(
                user.tipo_usuario, None
            )
            cotizacion_id_obj = CotizacionID.from_string(cotizacion_id)
            cotizacion = cotizacion_repo.find_by_id(cotizacion_id_obj)
            
            if not cotizacion:
                return JsonResponse({
                    'success': False,
                    'error': 'Cotización no encontrada'
                }, status=404)
            
            # Validar que la empresa puede eliminar esta cotización
            if cotizacion.empresa_id != user.user_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Solo puede eliminar sus propias cotizaciones'
                }, status=403)
            
            # Eliminar
            cotizacion_repo.delete(cotizacion_id_obj)
            
            return JsonResponse({
                'success': True,
                'message': 'Cotización eliminada exitosamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error interno: {str(e)}'
            }, status=500)
    
    def _serialize_cotizacion(self, cotizacion: Quotation) -> Dict[str, Any]:
        """Serializa una cotización para la respuesta JSON."""
        return {
            'cotizacion_id': str(cotizacion.cotizacion_id),
            'numero_cotizacion': cotizacion.numero_cotizacion,
            'empresa_id': cotizacion.empresa_id,
            'cliente_id': cotizacion.cliente_id,
            'estado': cotizacion.estado.value,
            'total': str(cotizacion.total),
            'fecha_creacion': cotizacion.fecha_creacion.isoformat(),
            'fecha_envio': cotizacion.fecha_envio.isoformat() if cotizacion.fecha_envio else None,
            'observaciones': cotizacion.observaciones,
            'equipos': [
                {
                    'name': equipo.name,
                    'brand': equipo.brand,
                    'model': equipo.model,
                    'description': equipo.description,
                    'price': str(equipo.price) if equipo.price else None,
                    'serial_number': equipo.serial_number
                }
                for equipo in cotizacion.equipos
            ]
        }
