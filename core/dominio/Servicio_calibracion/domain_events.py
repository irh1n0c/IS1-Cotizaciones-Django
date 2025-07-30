#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Callable
from dataclasses import dataclass


class DomainEvent(ABC):
    """Clase base para todos los domain events."""
    
    def __init__(self):
        self.occurred_on = datetime.now()
        self.event_id = self._generate_event_id()
    
    def _generate_event_id(self) -> str:
        """Genera un ID único para el evento."""
        import uuid
        return str(uuid.uuid4())
    
    @abstractmethod
    def get_event_data(self) -> Dict[str, Any]:
        """Retorna los datos del evento."""
        pass
    
    @property
    def event_type(self) -> str:
        """Retorna el tipo de evento."""
        return self.__class__.__name__


@dataclass
class CotizacionCreadaEvent(DomainEvent):
    """Evento que se dispara cuando se crea una cotización."""
    
    def __init__(self, cotizacion_id: str, empresa_id: str, cliente_id: str, numero_cotizacion: str):
        super().__init__()
        self.cotizacion_id = cotizacion_id
        self.empresa_id = empresa_id
        self.cliente_id = cliente_id
        self.numero_cotizacion = numero_cotizacion
    
    def get_event_data(self) -> Dict[str, Any]:
        return {
            "cotizacion_id": self.cotizacion_id,
            "empresa_id": self.empresa_id,
            "cliente_id": self.cliente_id,
            "numero_cotizacion": self.numero_cotizacion,
            "occurred_on": self.occurred_on.isoformat()
        }


@dataclass
class CotizacionEnviadaEvent(DomainEvent):
    """Evento que se dispara cuando se envía una cotización."""
    
    def __init__(self, cotizacion_id: str, cliente_id: str, numero_cotizacion: str, 
                 total: str, fecha_vencimiento: str):
        super().__init__()
        self.cotizacion_id = cotizacion_id
        self.cliente_id = cliente_id
        self.numero_cotizacion = numero_cotizacion
        self.total = total
        self.fecha_vencimiento = fecha_vencimiento
    
    def get_event_data(self) -> Dict[str, Any]:
        return {
            "cotizacion_id": self.cotizacion_id,
            "cliente_id": self.cliente_id,
            "numero_cotizacion": self.numero_cotizacion,
            "total": self.total,
            "fecha_vencimiento": self.fecha_vencimiento,
            "occurred_on": self.occurred_on.isoformat()
        }


@dataclass
class CotizacionAprobadaEvent(DomainEvent):
    """Evento que se dispara cuando se aprueba una cotización."""
    
    def __init__(self, cotizacion_id: str, cliente_id: str, empresa_id: str, 
                 numero_cotizacion: str, total: str):
        super().__init__()
        self.cotizacion_id = cotizacion_id
        self.cliente_id = cliente_id
        self.empresa_id = empresa_id
        self.numero_cotizacion = numero_cotizacion
        self.total = total
    
    def get_event_data(self) -> Dict[str, Any]:
        return {
            "cotizacion_id": self.cotizacion_id,
            "cliente_id": self.cliente_id,
            "empresa_id": self.empresa_id,
            "numero_cotizacion": self.numero_cotizacion,
            "total": self.total,
            "occurred_on": self.occurred_on.isoformat()
        }


@dataclass
class CotizacionRechazadaEvent(DomainEvent):
    """Evento que se dispara cuando se rechaza una cotización."""
    
    def __init__(self, cotizacion_id: str, cliente_id: str, empresa_id: str, 
                 numero_cotizacion: str, motivo: str):
        super().__init__()
        self.cotizacion_id = cotizacion_id
        self.cliente_id = cliente_id
        self.empresa_id = empresa_id
        self.numero_cotizacion = numero_cotizacion
        self.motivo = motivo
    
    def get_event_data(self) -> Dict[str, Any]:
        return {
            "cotizacion_id": self.cotizacion_id,
            "cliente_id": self.cliente_id,
            "empresa_id": self.empresa_id,
            "numero_cotizacion": self.numero_cotizacion,
            "motivo": self.motivo,
            "occurred_on": self.occurred_on.isoformat()
        }


@dataclass
class CotizacionVistaPorClienteEvent(DomainEvent):
    """Evento que se dispara cuando el cliente ve una cotización."""
    
    def __init__(self, cotizacion_id: str, cliente_id: str, numero_cotizacion: str):
        super().__init__()
        self.cotizacion_id = cotizacion_id
        self.cliente_id = cliente_id
        self.numero_cotizacion = numero_cotizacion
    
    def get_event_data(self) -> Dict[str, Any]:
        return {
            "cotizacion_id": self.cotizacion_id,
            "cliente_id": self.cliente_id,
            "numero_cotizacion": self.numero_cotizacion,
            "occurred_on": self.occurred_on.isoformat()
        }


@dataclass
class CotizacionVencidaEvent(DomainEvent):
    """Evento que se dispara cuando una cotización vence."""
    
    def __init__(self, cotizacion_id: str, cliente_id: str, empresa_id: str, numero_cotizacion: str):
        super().__init__()
        self.cotizacion_id = cotizacion_id
        self.cliente_id = cliente_id
        self.empresa_id = empresa_id
        self.numero_cotizacion = numero_cotizacion
    
    def get_event_data(self) -> Dict[str, Any]:
        return {
            "cotizacion_id": self.cotizacion_id,
            "cliente_id": self.cliente_id,
            "empresa_id": self.empresa_id,
            "numero_cotizacion": self.numero_cotizacion,
            "occurred_on": self.occurred_on.isoformat()
        }


class DomainEventHandler(ABC):
    """Interfaz para los manejadores de domain events."""
    
    @abstractmethod
    def handle(self, event: DomainEvent) -> None:
        """Maneja un domain event."""
        pass
    
    @abstractmethod
    def can_handle(self, event: DomainEvent) -> bool:
        """Indica si puede manejar el evento."""
        pass


class DomainEventDispatcher:
    """Despachador de domain events."""
    
    def __init__(self):
        self._handlers: List[DomainEventHandler] = []
        self._event_store: List[DomainEvent] = []
    
    def register_handler(self, handler: DomainEventHandler) -> None:
        """Registra un manejador de eventos."""
        self._handlers.append(handler)
    
    def dispatch(self, event: DomainEvent) -> None:
        """Despacha un evento a todos los manejadores apropiados."""
        # Almacenar el evento
        self._event_store.append(event)
        
        # Enviar a manejadores
        for handler in self._handlers:
            if handler.can_handle(event):
                try:
                    handler.handle(event)
                except Exception as e:
                    # Log del error pero no interrumpir el flujo
                    print(f"Error handling event {event.event_type}: {str(e)}")
    
    def get_events(self) -> List[DomainEvent]:
        """Obtiene todos los eventos almacenados."""
        return self._event_store.copy()
    
    def clear_events(self) -> None:
        """Limpia el almacén de eventos."""
        self._event_store.clear()


# Manejadores específicos de eventos

class NotificacionEventHandler(DomainEventHandler):
    """Manejador para enviar notificaciones basadas en eventos."""
    
    def __init__(self, notification_service):
        self._notification_service = notification_service
    
    def can_handle(self, event: DomainEvent) -> bool:
        """Puede manejar eventos de cotización."""
        return isinstance(event, (
            CotizacionEnviadaEvent,
            CotizacionAprobadaEvent,
            CotizacionRechazadaEvent,
            CotizacionVencidaEvent
        ))
    
    def handle(self, event: DomainEvent) -> None:
        """Maneja eventos enviando notificaciones."""
        if isinstance(event, CotizacionEnviadaEvent):
            self._notification_service.enviar_notificacion_cliente(
                event.cliente_id,
                f"Nueva cotización disponible: {event.numero_cotizacion}",
                event.get_event_data()
            )
        
        elif isinstance(event, CotizacionAprobadaEvent):
            self._notification_service.enviar_notificacion_empresa(
                event.empresa_id,
                f"Cotización aprobada: {event.numero_cotizacion}",
                event.get_event_data()
            )
        
        elif isinstance(event, CotizacionRechazadaEvent):
            self._notification_service.enviar_notificacion_empresa(
                event.empresa_id,
                f"Cotización rechazada: {event.numero_cotizacion}",
                event.get_event_data()
            )
        
        elif isinstance(event, CotizacionVencidaEvent):
            self._notification_service.enviar_notificacion_empresa(
                event.empresa_id,
                f"Cotización vencida: {event.numero_cotizacion}",
                event.get_event_data()
            )


class AuditoriaEventHandler(DomainEventHandler):
    """Manejador para auditoría de eventos."""
    
    def __init__(self, audit_service):
        self._audit_service = audit_service
    
    def can_handle(self, event: DomainEvent) -> bool:
        """Puede manejar todos los eventos para auditoría."""
        return True
    
    def handle(self, event: DomainEvent) -> None:
        """Registra el evento en el sistema de auditoría."""
        self._audit_service.log_event(
            event.event_type,
            event.get_event_data(),
            event.occurred_on
        )


class MetricasEventHandler(DomainEventHandler):
    """Manejador para métricas y analytics."""
    
    def __init__(self, metrics_service):
        self._metrics_service = metrics_service
    
    def can_handle(self, event: DomainEvent) -> bool:
        """Puede manejar eventos relevantes para métricas."""
        return isinstance(event, (
            CotizacionCreadaEvent,
            CotizacionEnviadaEvent,
            CotizacionAprobadaEvent,
            CotizacionRechazadaEvent
        ))
    
    def handle(self, event: DomainEvent) -> None:
        """Actualiza métricas basadas en el evento."""
        if isinstance(event, CotizacionCreadaEvent):
            self._metrics_service.increment_counter("cotizaciones_creadas")
        
        elif isinstance(event, CotizacionEnviadaEvent):
            self._metrics_service.increment_counter("cotizaciones_enviadas")
        
        elif isinstance(event, CotizacionAprobadaEvent):
            self._metrics_service.increment_counter("cotizaciones_aprobadas")
            # Registrar valor de venta
            self._metrics_service.record_sale_value(float(event.total))
        
        elif isinstance(event, CotizacionRechazadaEvent):
            self._metrics_service.increment_counter("cotizaciones_rechazadas")


# Singleton global del dispatcher
_global_dispatcher = DomainEventDispatcher()

def get_domain_event_dispatcher() -> DomainEventDispatcher:
    """Obtiene la instancia global del dispatcher."""
    return _global_dispatcher