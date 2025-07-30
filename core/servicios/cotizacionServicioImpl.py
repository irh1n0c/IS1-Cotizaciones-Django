#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List, Optional
from datetime import datetime
from core.dominio.Servicio_calibracion.quotation import Quotation, EquipmentDetails
from core.dominio.Servicio_calibracion.cotizacionID import CotizacionID
from core.dominio.Servicio_calibracion.estadoCotizacion import EstadoCotizacion, TipoUsuario
from core.dominio.Servicio_calibracion.usuario import Usuario
from core.dominio.Servicio_calibracion.number_quotation import QuotationNumberGenerator
from core.dominio.Servicio_calibracion.money import Money


class CotizacionServicioImpl:
    """Servicio de dominio para operaciones complejas de cotizaciones."""
    
    def __init__(self, cotizacion_repository, cliente_repository, notificacion_service):
        self._cotizacion_repository = cotizacion_repository
        self._cliente_repository = cliente_repository
        self._notificacion_service = notificacion_service
    
    def crear_cotizacion_dinamica(self, empresa_id: str, cliente_id: str,
                                 equipos: List[EquipmentDetails], usuario: Usuario) -> Quotation:
        """Crea una cotización completa con validaciones de negocio."""
        
        # Validar permisos
        if not usuario.puede_crear_cotizacion():
            raise ValueError("El usuario no tiene permisos para crear cotizaciones")
        
        if usuario.user_id != empresa_id:
            raise ValueError("Solo puede crear cotizaciones para su propia empresa")
        
        # Validar cliente existe
        cliente = self._cliente_repository.find_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente no encontrado")
        
        # Generar número de cotización
        numero_cotizacion = self._generar_numero_cotizacion()
        
        # Crear cotización
        cotizacion_id = CotizacionID.generate()
        cotizacion = Quotation(cotizacion_id, numero_cotizacion, empresa_id, cliente_id)
        
        # Agregar equipos
        for equipo in equipos:
            cotizacion.agregar_equipo(equipo, usuario.user_id, usuario.tipo_usuario)
        
        # Guardar
        self._cotizacion_repository.save(cotizacion)
        
        return cotizacion
    
    def procesar_aprobacion(self, cotizacion_id: CotizacionID, cliente_id: str) -> None:
        """Procesa la aprobación de una cotización por parte del cliente."""
        
        # Obtener cotización
        cotizacion = self._cotizacion_repository.find_by_id(cotizacion_id)
        if not cotizacion:
            raise ValueError("Cotización no encontrada")
        
        # Validar que el cliente puede aprobar
        if cotizacion.cliente_id != cliente_id:
            raise ValueError("Solo el cliente asignado puede aprobar la cotización")
        
        if not cotizacion.es_visible_para_cliente(cliente_id):
            raise ValueError("La cotización no está disponible para aprobación")
        
        # Aprobar
        cotizacion.aprobar()
        
        # Guardar
        self._cotizacion_repository.save(cotizacion)
        
        # Notificar a la empresa
        self._notificar_aprobacion(cotizacion)
    
    def procesar_rechazo(self, cotizacion_id: CotizacionID, cliente_id: str, motivo: str) -> None:
        """Procesa el rechazo de una cotización por parte del cliente."""
        
        # Obtener cotización
        cotizacion = self._cotizacion_repository.find_by_id(cotizacion_id)
        if not cotizacion:
            raise ValueError("Cotización no encontrada")
        
        # Validar que el cliente puede rechazar
        if cotizacion.cliente_id != cliente_id:
            raise ValueError("Solo el cliente asignado puede rechazar la cotización")
        
        # Rechazar
        cotizacion.rechazar(motivo)
        
        # Guardar
        self._cotizacion_repository.save(cotizacion)
        
        # Notificar a la empresa
        self._notificar_rechazo(cotizacion, motivo)
    
    def enviar_cotizacion(self, cotizacion_id: CotizacionID, usuario: Usuario) -> None:
        """Envía una cotización al cliente."""
        
        # Obtener cotización
        cotizacion = self._cotizacion_repository.find_by_id(cotizacion_id)
        if not cotizacion:
            raise ValueError("Cotización no encontrada")
        
        # Enviar
        cotizacion.enviar_cotizacion(usuario.user_id, usuario.tipo_usuario)
        
        # Guardar
        self._cotizacion_repository.save(cotizacion)
        
        # Notificar al cliente
        self._notificar_envio(cotizacion)
    
    def calcular_precio_total_con_descuentos(self, cotizacion: Quotation,
                                           descuento_porcentaje: float = 0) -> Money:
        """Calcula el precio total aplicando descuentos."""
        
        total_base = cotizacion.total
        
        if descuento_porcentaje > 0:
            total_con_descuento = total_base.apply_discount(descuento_porcentaje)
            return total_con_descuento
        
        return total_base
    
    def verificar_cotizaciones_vencidas(self) -> List[Quotation]:
        """Verifica y marca cotizaciones vencidas."""
        
        cotizaciones_activas = self._cotizacion_repository.find_by_estados([
            EstadoCotizacion.ENVIADA,
            EstadoCotizacion.VISTA_POR_CLIENTE
        ])
        
        cotizaciones_vencidas = []
        
        for cotizacion in cotizaciones_activas:
            cotizacion.verificar_vencimiento()
            if cotizacion.estado == EstadoCotizacion.VENCIDA:
                cotizaciones_vencidas.append(cotizacion)
                self._cotizacion_repository.save(cotizacion)
        
        return cotizaciones_vencidas
    
    def obtener_cotizaciones_para_empresa(self, empresa_id: str,
                                        estado: Optional[EstadoCotizacion] = None) -> List[Quotation]:
        """Obtiene cotizaciones de una empresa específica."""
        
        if estado:
            return self._cotizacion_repository.find_by_empresa_and_estado(empresa_id, estado)
        else:
            return self._cotizacion_repository.find_by_empresa(empresa_id)
    
    def obtener_cotizaciones_para_cliente(self, cliente_id: str) -> List[Quotation]:
        """Obtiene cotizaciones visibles para un cliente."""
        
        todas_cotizaciones = self._cotizacion_repository.find_by_cliente(cliente_id)
        
        # Filtrar solo las visibles para el cliente
        cotizaciones_visibles = []
        for cotizacion in todas_cotizaciones:
            if cotizacion.es_visible_para_cliente(cliente_id):
                cotizaciones_visibles.append(cotizacion)
        
        return cotizaciones_visibles
    
    def marcar_cotizacion_como_vista(self, cotizacion_id: CotizacionID, cliente_id: str) -> None:
        """Marca una cotización como vista por el cliente."""
        
        cotizacion = self._cotizacion_repository.find_by_id(cotizacion_id)
        if not cotizacion:
            raise ValueError("Cotización no encontrada")
        
        if cotizacion.cliente_id != cliente_id:
            raise ValueError("Solo el cliente asignado puede marcar como vista")
        
        cotizacion.marcar_como_vista_por_cliente()
        self._cotizacion_repository.save(cotizacion)
    
    def _generar_numero_cotizacion(self) -> str:
        """Genera un número único de cotización."""
        # Aquí podrías implementar lógica más compleja para generar números únicos
        # Por ahora usamos el generador existente con valores por defecto
        return QuotationNumberGenerator.generate()
    
    def _notificar_envio(self, cotizacion: Quotation) -> None:
        """Notifica al cliente sobre el envío de la cotización."""
        if self._notificacion_service:
            self._notificacion_service.notificar_envio_cotizacion(
                cotizacion.cliente_id,
                cotizacion.numero_cotizacion,
                cotizacion.total
            )
    
    def _notificar_aprobacion(self, cotizacion: Quotation) -> None:
        """Notifica a la empresa sobre la aprobación."""
        if self._notificacion_service:
            self._notificacion_service.notificar_aprobacion_cotizacion(
                cotizacion.empresa_id,
                cotizacion.numero_cotizacion,
                cotizacion.cliente_id
            )
    
    def _notificar_rechazo(self, cotizacion: Quotation, motivo: str) -> None:
        """Notifica a la empresa sobre el rechazo."""
        if self._notificacion_service:
            self._notificacion_service.notificar_rechazo_cotizacion(
                cotizacion.empresa_id,
                cotizacion.numero_cotizacion,
                cotizacion.cliente_id,
                motivo
            )
