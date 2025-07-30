"""
Módulo para manejo de detalles de equipos médicos.
Contiene la clase EquipmentDetails con validaciones y propiedades.
"""

import re
from typing import Optional
from datetime import datetime, timedelta


class EquipmentDetails:
    """Maneja los detalles del equipo médico con validaciones robustas."""
    
    def __init__(self):
        self._name = None
        self._brand = None
        self._model = None
        self._description = None
        self._price = None
        self._serial_number = None

    @property
    def name(self) -> Optional[str]:
        """Nombre del equipo médico."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Establece el nombre del equipo con validación."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre debe ser una cadena de texto no vacía")
        self._name = name.strip()

    @property
    def brand(self) -> Optional[str]:
        """Marca del equipo médico."""
        return self._brand

    @brand.setter
    def brand(self, brand: str) -> None:
        """Establece la marca del equipo con validación."""
        if not isinstance(brand, str) or not brand.strip():
            raise ValueError("La marca debe ser una cadena de texto no vacía")
        self._brand = brand.strip()

    @property
    def model(self) -> Optional[str]:
        """Modelo del equipo médico."""
        return self._model

    @model.setter
    def model(self, model: str) -> None:
        """Establece el modelo del equipo con validación."""
        if not isinstance(model, str) or not model.strip():
            raise ValueError("El modelo debe ser una cadena de texto no vacía")
        self._model = model.strip()

    @property
    def description(self) -> Optional[str]:
        """Descripción del equipo médico."""
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        """Establece la descripción del equipo (puede ser vacía)."""
        self._description = description.strip() if description else None

    @property
    def price(self) -> Optional[float]:
        """Precio del equipo médico."""
        return self._price

    @price.setter
    def price(self, price: float) -> None:
        """Establece el precio del equipo con validación."""
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("El precio debe ser un número positivo")
        self._price = float(price)

    @property
    def serial_number(self) -> Optional[str]:
        """Número de serie del equipo médico."""
        return self._serial_number

    @serial_number.setter
    def serial_number(self, serial_number: str) -> None:
        """Establece el número de serie con validación de formato."""
        if not self._is_valid_serial_number(serial_number):
            raise ValueError("El número de serie solo debe contener letras, números y guiones")
        self._serial_number = serial_number

    @staticmethod
    def _is_valid_serial_number(serial_number: str) -> bool:
        """Valida el formato del número de serie."""
        pattern = r'^[A-Za-z0-9-]+$'
        return bool(re.match(pattern, serial_number))

    def __str__(self) -> str:
        """Representación en cadena del equipo."""
        return (f"EquipmentDetails(name='{self.name}', brand='{self.brand}', "
                f"model='{self.model}', price={self.price})")

    def __repr__(self) -> str:
        """Representación oficial del equipo."""
        return self.__str__()


class Quotation:
    """Agregado raíz que representa una cotización completa."""
    
    def __init__(self, cotizacion_id: 'CotizacionID', numero_cotizacion: str,
                 empresa_id: str, cliente_id: str):
        from .cotizacionID import CotizacionID
        from .estadoCotizacion import EstadoCotizacion
        from .money import Money
        
        self._cotizacion_id = cotizacion_id
        self._numero_cotizacion = numero_cotizacion
        self._empresa_id = empresa_id
        self._cliente_id = cliente_id
        self._estado = EstadoCotizacion.BORRADOR
        self._equipos = []
        self._fecha_creacion = datetime.now()
        self._fecha_envio = None
        self._fecha_vencimiento = None
        self._total = Money.zero()
        self._observaciones = ""
        self._domain_events = []
    
    @property
    def cotizacion_id(self) -> 'CotizacionID':
        """ID único de la cotización."""
        return self._cotizacion_id
    
    @property
    def numero_cotizacion(self) -> str:
        """Número de cotización generado."""
        return self._numero_cotizacion
    
    @property
    def empresa_id(self) -> str:
        """ID de la empresa que crea la cotización."""
        return self._empresa_id
    
    @property
    def cliente_id(self) -> str:
        """ID del cliente para quien es la cotización."""
        return self._cliente_id
    
    @property
    def estado(self) -> 'EstadoCotizacion':
        """Estado actual de la cotización."""
        return self._estado
    
    @property
    def equipos(self) -> list:
        """Lista de equipos en la cotización."""
        return self._equipos.copy()
    
    @property
    def total(self) -> 'Money':
        """Total de la cotización."""
        return self._total
    
    @property
    def fecha_creacion(self) -> datetime:
        """Fecha de creación de la cotización."""
        return self._fecha_creacion
    
    @property
    def fecha_envio(self) -> Optional[datetime]:
        """Fecha de envío de la cotización."""
        return self._fecha_envio
    
    @property
    def observaciones(self) -> str:
        """Observaciones de la cotización."""
        return self._observaciones
    
    def puede_ser_modificada_por(self, usuario_id: str, tipo_usuario: 'TipoUsuario') -> bool:
        """Verifica si un usuario puede modificar esta cotización."""
        from .estadoCotizacion import TipoUsuario
        
        # Solo la empresa puede modificar
        if tipo_usuario != TipoUsuario.EMPRESA:
            return False
        
        # Solo la empresa propietaria puede modificar
        if self._empresa_id != usuario_id:
            return False
        
        # Solo se puede modificar en estado borrador
        return self._estado.permite_modificacion()
    
    def agregar_equipo(self, equipo: EquipmentDetails, usuario_id: str, tipo_usuario: 'TipoUsuario') -> None:
        """Agrega un equipo a la cotización."""
        if not self.puede_ser_modificada_por(usuario_id, tipo_usuario):
            raise ValueError("No tiene permisos para modificar esta cotización")
        
        if not isinstance(equipo, EquipmentDetails):
            raise ValueError("El equipo debe ser una instancia de EquipmentDetails")
        
        self._equipos.append(equipo)
        self._recalcular_total()
        
        # Agregar domain event
        self._add_domain_event("EquipoAgregado", {
            "cotizacion_id": str(self._cotizacion_id),
            "equipo_nombre": equipo.name,
            "precio": str(equipo.price)
        })
    
    def remover_equipo(self, indice: int, usuario_id: str, tipo_usuario: 'TipoUsuario') -> None:
        """Remueve un equipo de la cotización."""
        if not self.puede_ser_modificada_por(usuario_id, tipo_usuario):
            raise ValueError("No tiene permisos para modificar esta cotización")
        
        if indice < 0 or indice >= len(self._equipos):
            raise ValueError("Índice de equipo inválido")
        
        equipo_removido = self._equipos.pop(indice)
        self._recalcular_total()
        
        # Agregar domain event
        self._add_domain_event("EquipoRemovido", {
            "cotizacion_id": str(self._cotizacion_id),
            "equipo_nombre": equipo_removido.name
        })
    
    def enviar_cotizacion(self, usuario_id: str, tipo_usuario: 'TipoUsuario') -> None:
        """Envía la cotización al cliente."""
        from .estadoCotizacion import EstadoCotizacion, TipoUsuario
        
        if not self.puede_ser_modificada_por(usuario_id, tipo_usuario):
            raise ValueError("No tiene permisos para enviar esta cotización")
        
        if not self._equipos:
            raise ValueError("No se puede enviar una cotización sin equipos")
        
        if not self._estado.puede_transicionar_a(EstadoCotizacion.ENVIADA):
            raise ValueError(f"No se puede enviar desde el estado {self._estado.value}")
        
        self._estado = EstadoCotizacion.ENVIADA
        self._fecha_envio = datetime.now()
        self._fecha_vencimiento = self._fecha_envio + timedelta(days=30)  # 30 días de vigencia
        
        # Agregar domain event
        self._add_domain_event("CotizacionEnviada", {
            "cotizacion_id": str(self._cotizacion_id),
            "cliente_id": self._cliente_id,
            "fecha_envio": self._fecha_envio.isoformat(),
            "fecha_vencimiento": self._fecha_vencimiento.isoformat()
        })
    
    def marcar_como_vista_por_cliente(self) -> None:
        """Marca la cotización como vista por el cliente."""
        from .estadoCotizacion import EstadoCotizacion
        
        if self._estado == EstadoCotizacion.ENVIADA:
            if self._estado.puede_transicionar_a(EstadoCotizacion.VISTA_POR_CLIENTE):
                self._estado = EstadoCotizacion.VISTA_POR_CLIENTE
                
                # Agregar domain event
                self._add_domain_event("CotizacionVistaPorCliente", {
                    "cotizacion_id": str(self._cotizacion_id),
                    "cliente_id": self._cliente_id,
                    "fecha_vista": datetime.now().isoformat()
                })
    
    def aprobar(self) -> None:
        """Aprueba la cotización (acción del cliente)."""
        from .estadoCotizacion import EstadoCotizacion
        
        if not self._estado.puede_transicionar_a(EstadoCotizacion.APROBADA):
            raise ValueError(f"No se puede aprobar desde el estado {self._estado.value}")
        
        self._estado = EstadoCotizacion.APROBADA
        
        # Agregar domain event
        self._add_domain_event("CotizacionAprobada", {
            "cotizacion_id": str(self._cotizacion_id),
            "cliente_id": self._cliente_id,
            "total": str(self._total),
            "fecha_aprobacion": datetime.now().isoformat()
        })
    
    def rechazar(self, motivo: str = "") -> None:
        """Rechaza la cotización (acción del cliente)."""
        from .estadoCotizacion import EstadoCotizacion
        
        if not self._estado.puede_transicionar_a(EstadoCotizacion.RECHAZADA):
            raise ValueError(f"No se puede rechazar desde el estado {self._estado.value}")
        
        self._estado = EstadoCotizacion.RECHAZADA
        if motivo:
            self._observaciones = f"Rechazada: {motivo}"
        
        # Agregar domain event
        self._add_domain_event("CotizacionRechazada", {
            "cotizacion_id": str(self._cotizacion_id),
            "cliente_id": self._cliente_id,
            "motivo": motivo,
            "fecha_rechazo": datetime.now().isoformat()
        })
    
    def cancelar(self, usuario_id: str, tipo_usuario: 'TipoUsuario', motivo: str = "") -> None:
        """Cancela la cotización (acción de la empresa)."""
        from .estadoCotizacion import EstadoCotizacion, TipoUsuario
        
        if tipo_usuario != TipoUsuario.EMPRESA or self._empresa_id != usuario_id:
            raise ValueError("Solo la empresa propietaria puede cancelar la cotización")
        
        if not self._estado.puede_transicionar_a(EstadoCotizacion.CANCELADA):
            raise ValueError(f"No se puede cancelar desde el estado {self._estado.value}")
        
        self._estado = EstadoCotizacion.CANCELADA
        if motivo:
            self._observaciones = f"Cancelada: {motivo}"
        
        # Agregar domain event
        self._add_domain_event("CotizacionCancelada", {
            "cotizacion_id": str(self._cotizacion_id),
            "empresa_id": self._empresa_id,
            "motivo": motivo,
            "fecha_cancelacion": datetime.now().isoformat()
        })
    
    def verificar_vencimiento(self) -> None:
        """Verifica si la cotización ha vencido."""
        from .estadoCotizacion import EstadoCotizacion
        
        if (self._fecha_vencimiento and
            datetime.now() > self._fecha_vencimiento and
            self._estado in [EstadoCotizacion.ENVIADA, EstadoCotizacion.VISTA_POR_CLIENTE]):
            
            self._estado = EstadoCotizacion.VENCIDA
            
            # Agregar domain event
            self._add_domain_event("CotizacionVencida", {
                "cotizacion_id": str(self._cotizacion_id),
                "fecha_vencimiento": self._fecha_vencimiento.isoformat()
            })
    
    def es_visible_para_cliente(self, cliente_id: str) -> bool:
        """Verifica si la cotización es visible para un cliente específico."""
        from .estadoCotizacion import EstadoCotizacion
        
        if self._cliente_id != cliente_id:
            return False
        
        return self._estado in EstadoCotizacion.estados_visibles_para_cliente()
    
    def agregar_observaciones(self, observaciones: str, usuario_id: str, tipo_usuario: 'TipoUsuario') -> None:
        """Agrega observaciones a la cotización."""
        if not self.puede_ser_modificada_por(usuario_id, tipo_usuario):
            raise ValueError("No tiene permisos para modificar esta cotización")
        
        self._observaciones = observaciones.strip()
    
    def _recalcular_total(self) -> None:
        """Recalcula el total de la cotización."""
        from .money import Money
        
        total = Money.zero()
        for equipo in self._equipos:
            if equipo.price is not None:
                precio_equipo = Money(equipo.price)
                total = total.add(precio_equipo)
        
        self._total = total
    
    def _add_domain_event(self, event_type: str, data: dict) -> None:
        """Agrega un domain event."""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self._domain_events.append(event)
    
    def get_domain_events(self) -> list:
        """Obtiene los domain events."""
        return self._domain_events.copy()
    
    def clear_domain_events(self) -> None:
        """Limpia los domain events."""
        self._domain_events.clear()
    
    def __str__(self) -> str:
        return f"Quotation({self._numero_cotizacion}, {self._estado.value}, {self._total})"
    
    def __repr__(self) -> str:
        return self.__str__()