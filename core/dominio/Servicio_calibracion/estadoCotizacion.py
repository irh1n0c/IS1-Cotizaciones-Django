#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum
from datetime import datetime, timedelta
from typing import List


class EstadoCotizacion(Enum):
    """Estados posibles de una cotización en el sistema."""
    
    BORRADOR = "borrador"
    ENVIADA = "enviada"
    VISTA_POR_CLIENTE = "vista_por_cliente"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"
    VENCIDA = "vencida"
    CANCELADA = "cancelada"

    def puede_transicionar_a(self, nuevo_estado: 'EstadoCotizacion') -> bool:
        """Define las transiciones válidas entre estados."""
        transiciones_validas = {
            EstadoCotizacion.BORRADOR: [
                EstadoCotizacion.ENVIADA,
                EstadoCotizacion.CANCELADA
            ],
            EstadoCotizacion.ENVIADA: [
                EstadoCotizacion.VISTA_POR_CLIENTE,
                EstadoCotizacion.VENCIDA,
                EstadoCotizacion.CANCELADA
            ],
            EstadoCotizacion.VISTA_POR_CLIENTE: [
                EstadoCotizacion.APROBADA,
                EstadoCotizacion.RECHAZADA,
                EstadoCotizacion.VENCIDA
            ],
            EstadoCotizacion.APROBADA: [],  # Estado final
            EstadoCotizacion.RECHAZADA: [
                EstadoCotizacion.BORRADOR  # Puede volver a editarse
            ],
            EstadoCotizacion.VENCIDA: [
                EstadoCotizacion.BORRADOR  # Puede renovarse
            ],
            EstadoCotizacion.CANCELADA: []  # Estado final
        }
        
        return nuevo_estado in transiciones_validas.get(self, [])

    def es_estado_final(self) -> bool:
        """Indica si el estado es final (no permite más transiciones)."""
        return self in [EstadoCotizacion.APROBADA, EstadoCotizacion.CANCELADA]

    def permite_modificacion(self) -> bool:
        """Indica si el estado permite modificar la cotización."""
        return self == EstadoCotizacion.BORRADOR

    @classmethod
    def estados_visibles_para_cliente(cls) -> List['EstadoCotizacion']:
        """Estados que el cliente puede ver."""
        return [
            cls.ENVIADA,
            cls.VISTA_POR_CLIENTE,
            cls.APROBADA,
            cls.RECHAZADA,
            cls.VENCIDA
        ]


class TipoUsuario(Enum):
    """Tipos de usuario en el sistema."""
    
    EMPRESA = "empresa"
    CLIENTE = "cliente"
    
    def puede_crear_cotizacion(self) -> bool:
        """Indica si el tipo de usuario puede crear cotizaciones."""
        return self == TipoUsuario.EMPRESA
    
    def puede_modificar_cotizacion(self) -> bool:
        """Indica si el tipo de usuario puede modificar cotizaciones."""
        return self == TipoUsuario.EMPRESA
    
    def puede_eliminar_cotizacion(self) -> bool:
        """Indica si el tipo de usuario puede eliminar cotizaciones."""
        return self == TipoUsuario.EMPRESA
