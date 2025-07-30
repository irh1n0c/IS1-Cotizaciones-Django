#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Configuración y setup para la arquitectura DDD del sistema de cotizaciones.
Este archivo centraliza la configuración de todos los componentes DDD.
"""

from typing import Dict, Any
from core.dominio.Servicio_calibracion.domain_events import (
    get_domain_event_dispatcher,
    NotificacionEventHandler,
    AuditoriaEventHandler,
    MetricasEventHandler
)
from core.servicios.repositories import RepositoryFactory


class DDDConfiguration:
    """Configuración central para la arquitectura DDD."""
    
    def __init__(self):
        self._initialized = False
        self._repository_factory = None
        self._domain_event_dispatcher = None
        self._services = {}
    
    def initialize(self, config: Dict[str, Any] = None) -> None:
        """Inicializa todos los componentes DDD."""
        if self._initialized:
            return
        
        config = config or {}
        
        # Inicializar factory de repositorios
        self._repository_factory = RepositoryFactory()
        
        # Inicializar dispatcher de eventos
        self._domain_event_dispatcher = get_domain_event_dispatcher()
        
        # Configurar manejadores de eventos
        self._setup_event_handlers(config)
        
        # Inicializar servicios
        self._setup_services(config)
        
        self._initialized = True
    
    def _setup_event_handlers(self, config: Dict[str, Any]) -> None:
        """Configura los manejadores de domain events."""
        
        # Manejador de notificaciones
        if config.get('enable_notifications', True):
            notification_service = self._get_notification_service(config)
            if notification_service:
                notification_handler = NotificacionEventHandler(notification_service)
                self._domain_event_dispatcher.register_handler(notification_handler)
        
        # Manejador de auditoría
        if config.get('enable_audit', True):
            audit_service = self._get_audit_service(config)
            if audit_service:
                audit_handler = AuditoriaEventHandler(audit_service)
                self._domain_event_dispatcher.register_handler(audit_handler)
        
        # Manejador de métricas
        if config.get('enable_metrics', True):
            metrics_service = self._get_metrics_service(config)
            if metrics_service:
                metrics_handler = MetricasEventHandler(metrics_service)
                self._domain_event_dispatcher.register_handler(metrics_handler)
    
    def _setup_services(self, config: Dict[str, Any]) -> None:
        """Inicializa los servicios de dominio."""
        # Los servicios se crearán dinámicamente cuando se necesiten
        # para evitar problemas de inicialización con tipos de usuario None
        self._services = {}
        print("[OK] Services configured for dynamic creation")
    
    def _get_notification_service(self, config: Dict[str, Any]):
        """Obtiene el servicio de notificaciones."""
        # Aquí se integraría con el servicio real de notificaciones
        # Por ahora retornamos un mock
        return MockNotificationService()
    
    def _get_audit_service(self, config: Dict[str, Any]):
        """Obtiene el servicio de auditoría."""
        # Aquí se integraría con el servicio real de auditoría
        return MockAuditService()
    
    def _get_metrics_service(self, config: Dict[str, Any]):
        """Obtiene el servicio de métricas."""
        # Aquí se integraría con el servicio real de métricas
        return MockMetricsService()
    
    @property
    def repository_factory(self) -> RepositoryFactory:
        """Obtiene la factory de repositorios."""
        if not self._initialized:
            raise RuntimeError("DDD Configuration not initialized")
        return self._repository_factory
    
    @property
    def domain_event_dispatcher(self):
        """Obtiene el dispatcher de eventos."""
        if not self._initialized:
            raise RuntimeError("DDD Configuration not initialized")
        return self._domain_event_dispatcher
    
    def get_service(self, service_name: str):
        """Obtiene un servicio por nombre."""
        if not self._initialized:
            raise RuntimeError("DDD Configuration not initialized")
        return self._services.get(service_name)


# Servicios mock para desarrollo/testing

class MockNotificationService:
    """Servicio mock de notificaciones."""
    
    def enviar_notificacion_cliente(self, cliente_id: str, mensaje: str, data: Dict[str, Any]):
        """Envía notificación a un cliente."""
        print(f"[NOTIFICATION] Cliente {cliente_id}: {mensaje}")
    
    def enviar_notificacion_empresa(self, empresa_id: str, mensaje: str, data: Dict[str, Any]):
        """Envía notificación a una empresa."""
        print(f"[NOTIFICATION] Empresa {empresa_id}: {mensaje}")
    
    def notificar_envio_cotizacion(self, cliente_id: str, numero_cotizacion: str, total):
        """Notifica envío de cotización."""
        print(f"[NOTIFICATION] Cotización {numero_cotizacion} enviada a cliente {cliente_id}")
    
    def notificar_aprobacion_cotizacion(self, empresa_id: str, numero_cotizacion: str, cliente_id: str):
        """Notifica aprobación de cotización."""
        print(f"[NOTIFICATION] Cotización {numero_cotizacion} aprobada por cliente {cliente_id}")
    
    def notificar_rechazo_cotizacion(self, empresa_id: str, numero_cotizacion: str, cliente_id: str, motivo: str):
        """Notifica rechazo de cotización."""
        print(f"[NOTIFICATION] Cotización {numero_cotizacion} rechazada por cliente {cliente_id}: {motivo}")


class MockAuditService:
    """Servicio mock de auditoría."""
    
    def log_event(self, event_type: str, data: Dict[str, Any], timestamp):
        """Registra un evento de auditoría."""
        print(f"[AUDIT] {timestamp}: {event_type} - {data}")


class MockMetricsService:
    """Servicio mock de métricas."""
    
    def increment_counter(self, counter_name: str):
        """Incrementa un contador."""
        print(f"[METRICS] Counter {counter_name} incremented")
    
    def record_sale_value(self, value: float):
        """Registra un valor de venta."""
        print(f"[METRICS] Sale recorded: ${value}")


# Instancia global de configuración
_global_config = DDDConfiguration()

def get_ddd_config() -> DDDConfiguration:
    """Obtiene la configuración global de DDD."""
    return _global_config

def initialize_ddd(config: Dict[str, Any] = None) -> None:
    """Inicializa la configuración DDD global."""
    _global_config.initialize(config)


# Funciones de conveniencia para obtener componentes

def get_repository_factory() -> RepositoryFactory:
    """Obtiene la factory de repositorios."""
    return _global_config.repository_factory

def get_cotizacion_service(tipo_usuario=None):
    """Obtiene el servicio de cotizaciones, creándolo dinámicamente si es necesario."""
    service = _global_config.get_service('cotizacion_service')
    if service is None and tipo_usuario is not None:
        # Crear servicio dinámicamente
        from core.servicios.cotizacionServicioImpl import CotizacionServicioImpl
        
        cotizacion_repo = _global_config.repository_factory.create_cotizacion_repository(
            tipo_usuario, None
        )
        cliente_repo = _global_config.repository_factory.create_cliente_repository(None)
        notification_service = MockNotificationService()
        
        service = CotizacionServicioImpl(cotizacion_repo, cliente_repo, notification_service)
        _global_config._services['cotizacion_service'] = service
    
    return service

def dispatch_domain_event(event):
    """Despacha un domain event."""
    _global_config.domain_event_dispatcher.dispatch(event)


# Decorador para asegurar inicialización DDD

def requires_ddd_initialization(func):
    """Decorador que asegura que DDD esté inicializado."""
    def wrapper(*args, **kwargs):
        if not _global_config._initialized:
            initialize_ddd()
        return func(*args, **kwargs)
    return wrapper


# Configuración por defecto para Django

def setup_django_ddd():
    """Configura DDD para Django."""
    from django.conf import settings
    
    config = {
        'enable_notifications': getattr(settings, 'DDD_ENABLE_NOTIFICATIONS', True),
        'enable_audit': getattr(settings, 'DDD_ENABLE_AUDIT', True),
        'enable_metrics': getattr(settings, 'DDD_ENABLE_METRICS', True),
    }
    
    initialize_ddd(config)