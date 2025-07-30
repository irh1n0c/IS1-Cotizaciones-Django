#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional
from .estadoCotizacion import TipoUsuario


class Usuario:
    """Entidad que representa un usuario del sistema."""
    
    def __init__(self, user_id: str, email: str, tipo_usuario: TipoUsuario,
                 password_hash: str, nombre_completo: str):
        self._validate_inputs(user_id, email, password_hash, nombre_completo)
        
        self._user_id = user_id
        self._email = email.lower().strip()
        self._tipo_usuario = tipo_usuario
        self._password_hash = password_hash
        self._nombre_completo = nombre_completo.strip()
        self._login_status = False
        self._register_date = datetime.now()
        self._last_login = None
        self._is_active = True
    
    @staticmethod
    def _validate_inputs(user_id: str, email: str, password_hash: str, nombre_completo: str):
        """Valida los datos de entrada."""
        if not user_id or not isinstance(user_id, str):
            raise ValueError("El ID de usuario es requerido")
        
        if not email or not isinstance(email, str) or '@' not in email:
            raise ValueError("El email debe ser válido")
        
        if not password_hash or not isinstance(password_hash, str):
            raise ValueError("El hash de contraseña es requerido")
        
        if not nombre_completo or not isinstance(nombre_completo, str):
            raise ValueError("El nombre completo es requerido")
    
    @property
    def user_id(self) -> str:
        """ID único del usuario."""
        return self._user_id
    
    @property
    def email(self) -> str:
        """Email del usuario."""
        return self._email
    
    @property
    def tipo_usuario(self) -> TipoUsuario:
        """Tipo de usuario (EMPRESA o CLIENTE)."""
        return self._tipo_usuario
    
    @property
    def nombre_completo(self) -> str:
        """Nombre completo del usuario."""
        return self._nombre_completo
    
    @property
    def is_logged_in(self) -> bool:
        """Estado de login del usuario."""
        return self._login_status
    
    @property
    def register_date(self) -> datetime:
        """Fecha de registro del usuario."""
        return self._register_date
    
    @property
    def last_login(self) -> Optional[datetime]:
        """Última fecha de login."""
        return self._last_login
    
    @property
    def is_active(self) -> bool:
        """Indica si el usuario está activo."""
        return self._is_active
    
    def verificar_login(self, password_hash: str) -> bool:
        """Verifica las credenciales de login."""
        if not self._is_active:
            raise ValueError("Usuario inactivo")
        
        if self._password_hash == password_hash:
            self._login_status = True
            self._last_login = datetime.now()
            return True
        return False
    
    def logout(self) -> None:
        """Cierra la sesión del usuario."""
        self._login_status = False
    
    def puede_crear_cotizacion(self) -> bool:
        """Indica si el usuario puede crear cotizaciones."""
        return self._tipo_usuario.puede_crear_cotizacion() and self._is_active
    
    def puede_modificar_cotizacion(self) -> bool:
        """Indica si el usuario puede modificar cotizaciones."""
        return self._tipo_usuario.puede_modificar_cotizacion() and self._is_active
    
    def puede_eliminar_cotizacion(self) -> bool:
        """Indica si el usuario puede eliminar cotizaciones."""
        return self._tipo_usuario.puede_eliminar_cotizacion() and self._is_active
    
    def es_empresa(self) -> bool:
        """Indica si el usuario es de tipo empresa."""
        return self._tipo_usuario == TipoUsuario.EMPRESA
    
    def es_cliente(self) -> bool:
        """Indica si el usuario es de tipo cliente."""
        return self._tipo_usuario == TipoUsuario.CLIENTE
    
    def desactivar(self) -> None:
        """Desactiva el usuario."""
        self._is_active = False
        self._login_status = False
    
    def activar(self) -> None:
        """Activa el usuario."""
        self._is_active = True
    
    def cambiar_password(self, nuevo_password_hash: str) -> None:
        """Cambia la contraseña del usuario."""
        if not nuevo_password_hash or not isinstance(nuevo_password_hash, str):
            raise ValueError("El nuevo hash de contraseña es requerido")
        
        self._password_hash = nuevo_password_hash
    
    def __str__(self) -> str:
        return f"Usuario({self._user_id}, {self._email}, {self._tipo_usuario.value})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Usuario):
            return False
        return self._user_id == other._user_id
    
    def __hash__(self) -> int:
        return hash(self._user_id)
