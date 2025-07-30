#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, Optional
from core.dominio.Servicio_calibracion.quotation import Quotation
from core.dominio.Servicio_calibracion.cotizacionID import CotizacionID
from core.dominio.Servicio_calibracion.estadoCotizacion import EstadoCotizacion
from core.dominio.Servicio_calibracion.usuario import Usuario
from core.dominio.Servicio_calibracion.clienteClinica import ClienteClinica


class ICotizacionRepository(ABC):
    """Interfaz del repositorio de cotizaciones."""
    
    @abstractmethod
    def save(self, cotizacion: Quotation) -> None:
        """Guarda una cotización."""
        pass
    
    @abstractmethod
    def find_by_id(self, cotizacion_id: CotizacionID) -> Optional[Quotation]:
        """Busca una cotización por ID."""
        pass
    
    @abstractmethod
    def find_by_numero(self, numero_cotizacion: str) -> Optional[Quotation]:
        """Busca una cotización por número."""
        pass
    
    @abstractmethod
    def find_by_empresa(self, empresa_id: str) -> List[Quotation]:
        """Busca cotizaciones de una empresa."""
        pass
    
    @abstractmethod
    def find_by_cliente(self, cliente_id: str) -> List[Quotation]:
        """Busca cotizaciones de un cliente."""
        pass
    
    @abstractmethod
    def find_by_empresa_and_estado(self, empresa_id: str, estado: EstadoCotizacion) -> List[Quotation]:
        """Busca cotizaciones de una empresa por estado."""
        pass
    
    @abstractmethod
    def find_by_estados(self, estados: List[EstadoCotizacion]) -> List[Quotation]:
        """Busca cotizaciones por estados."""
        pass
    
    @abstractmethod
    def delete(self, cotizacion_id: CotizacionID) -> None:
        """Elimina una cotización."""
        pass


class IUsuarioRepository(ABC):
    """Interfaz del repositorio de usuarios."""
    
    @abstractmethod
    def save(self, usuario: Usuario) -> None:
        """Guarda un usuario."""
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[Usuario]:
        """Busca un usuario por ID."""
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Busca un usuario por email."""
        pass
    
    @abstractmethod
    def find_all_active(self) -> List[Usuario]:
        """Busca todos los usuarios activos."""
        pass


class IClienteRepository(ABC):
    """Interfaz del repositorio de clientes."""
    
    @abstractmethod
    def save(self, cliente: ClienteClinica) -> None:
        """Guarda un cliente."""
        pass
    
    @abstractmethod
    def find_by_id(self, cliente_id: str) -> Optional[ClienteClinica]:
        """Busca un cliente por ID."""
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[ClienteClinica]:
        """Busca un cliente por email."""
        pass
    
    @abstractmethod
    def find_all_active(self) -> List[ClienteClinica]:
        """Busca todos los clientes activos."""
        pass


# Implementaciones específicas para contextos

class EmpresaCotizacionRepository(ICotizacionRepository):
    """Repositorio de cotizaciones para el contexto de empresa."""
    
    def __init__(self, django_model_class):
        self._model = django_model_class
    
    def save(self, cotizacion: Quotation) -> None:
        """Guarda una cotización (implementación específica para empresa)."""
        # Aquí iría la lógica específica para guardar desde el contexto empresa
        # Podría incluir validaciones adicionales, logging, etc.
        pass
    
    def find_by_id(self, cotizacion_id: CotizacionID) -> Optional[Quotation]:
        """Busca cotización por ID con permisos de empresa."""
        # Implementación específica que podría incluir más datos
        pass
    
    def find_by_numero(self, numero_cotizacion: str) -> Optional[Quotation]:
        """Busca cotización por número."""
        pass
    
    def find_by_empresa(self, empresa_id: str) -> List[Quotation]:
        """Busca todas las cotizaciones de una empresa."""
        pass
    
    def find_by_cliente(self, cliente_id: str) -> List[Quotation]:
        """Busca cotizaciones de un cliente (vista empresa)."""
        pass
    
    def find_by_empresa_and_estado(self, empresa_id: str, estado: EstadoCotizacion) -> List[Quotation]:
        """Busca cotizaciones de empresa por estado."""
        pass
    
    def find_by_estados(self, estados: List[EstadoCotizacion]) -> List[Quotation]:
        """Busca cotizaciones por estados."""
        pass
    
    def delete(self, cotizacion_id: CotizacionID) -> None:
        """Elimina una cotización (solo empresas pueden eliminar)."""
        pass


class ClienteCotizacionRepository(ICotizacionRepository):
    """Repositorio de cotizaciones para el contexto de cliente."""
    
    def __init__(self, django_model_class):
        self._model = django_model_class
    
    def save(self, cotizacion: Quotation) -> None:
        """Los clientes no pueden guardar cotizaciones directamente."""
        raise NotImplementedError("Los clientes no pueden crear cotizaciones")
    
    def find_by_id(self, cotizacion_id: CotizacionID) -> Optional[Quotation]:
        """Busca cotización por ID (solo si es visible para cliente)."""
        pass
    
    def find_by_numero(self, numero_cotizacion: str) -> Optional[Quotation]:
        """Busca cotización por número (solo si es visible para cliente)."""
        pass
    
    def find_by_empresa(self, empresa_id: str) -> List[Quotation]:
        """Los clientes no pueden buscar por empresa."""
        raise NotImplementedError("Los clientes no pueden buscar por empresa")
    
    def find_by_cliente(self, cliente_id: str) -> List[Quotation]:
        """Busca cotizaciones del cliente (solo las visibles)."""
        pass
    
    def find_by_empresa_and_estado(self, empresa_id: str, estado: EstadoCotizacion) -> List[Quotation]:
        """Los clientes no pueden buscar por empresa y estado."""
        raise NotImplementedError("Los clientes no pueden buscar por empresa")
    
    def find_by_estados(self, estados: List[EstadoCotizacion]) -> List[Quotation]:
        """Busca cotizaciones por estados (solo estados visibles para cliente)."""
        estados_visibles = EstadoCotizacion.estados_visibles_para_cliente()
        estados_filtrados = [e for e in estados if e in estados_visibles]
        # Implementar búsqueda con estados filtrados
        pass
    
    def delete(self, cotizacion_id: CotizacionID) -> None:
        """Los clientes no pueden eliminar cotizaciones."""
        raise NotImplementedError("Los clientes no pueden eliminar cotizaciones")


class UsuarioRepository(IUsuarioRepository):
    """Implementación del repositorio de usuarios."""
    
    def __init__(self, django_model_class):
        self._model = django_model_class
    
    def save(self, usuario: Usuario) -> None:
        """Guarda un usuario."""
        pass
    
    def find_by_id(self, user_id: str) -> Optional[Usuario]:
        """Busca usuario por ID."""
        pass
    
    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Busca usuario por email."""
        pass
    
    def find_all_active(self) -> List[Usuario]:
        """Busca todos los usuarios activos."""
        pass


class ClienteRepository(IClienteRepository):
    """Implementación del repositorio de clientes."""
    
    def __init__(self, django_model_class):
        self._model = django_model_class
    
    def save(self, cliente: ClienteClinica) -> None:
        """Guarda un cliente."""
        pass
    
    def find_by_id(self, cliente_id: str) -> Optional[ClienteClinica]:
        """Busca cliente por ID."""
        pass
    
    def find_by_email(self, email: str) -> Optional[ClienteClinica]:
        """Busca cliente por email."""
        pass
    
    def find_all_active(self) -> List[ClienteClinica]:
        """Busca todos los clientes activos."""
        pass


# Factory para crear repositorios según el contexto
class RepositoryFactory:
    """Factory para crear repositorios según el contexto del usuario."""
    
    @staticmethod
    def create_cotizacion_repository(tipo_usuario, django_model_class):
        """Crea el repositorio apropiado según el tipo de usuario."""
        from core.dominio.Servicio_calibracion.estadoCotizacion import TipoUsuario
        
        if tipo_usuario == TipoUsuario.EMPRESA:
            return EmpresaCotizacionRepository(django_model_class)
        elif tipo_usuario == TipoUsuario.CLIENTE:
            return ClienteCotizacionRepository(django_model_class)
        else:
            raise ValueError(f"Tipo de usuario no soportado: {tipo_usuario}")
    
    @staticmethod
    def create_usuario_repository(django_model_class):
        """Crea el repositorio de usuarios."""
        return UsuarioRepository(django_model_class)
    
    @staticmethod
    def create_cliente_repository(django_model_class):
        """Crea el repositorio de clientes."""
        return ClienteRepository(django_model_class)