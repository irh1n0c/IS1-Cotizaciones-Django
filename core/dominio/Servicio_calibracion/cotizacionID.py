#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
from typing import Optional


class CotizacionID:
    """Value Object que representa el identificador único de una cotización."""
    
    def __init__(self, value: Optional[str] = None):
        if value is None:
            self._value = str(uuid.uuid4())
        else:
            self._validate(value)
            self._value = value
    
    @staticmethod
    def _validate(value: str) -> None:
        """Valida que el ID tenga el formato correcto."""
        if not isinstance(value, str):
            raise ValueError("El ID debe ser una cadena de texto")
        
        if not value.strip():
            raise ValueError("El ID no puede estar vacío")
        
        # Validar formato UUID si es necesario
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError("El ID debe tener formato UUID válido")
    
    @property
    def value(self) -> str:
        """Retorna el valor del ID."""
        return self._value
    
    def __str__(self) -> str:
        return self._value
    
    def __repr__(self) -> str:
        return f"CotizacionID('{self._value}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, CotizacionID):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        return hash(self._value)
    
    @classmethod
    def from_string(cls, value: str) -> 'CotizacionID':
        """Crea un CotizacionID desde un string."""
        return cls(value)
    
    @classmethod
    def generate(cls) -> 'CotizacionID':
        """Genera un nuevo CotizacionID único."""
        return cls()
