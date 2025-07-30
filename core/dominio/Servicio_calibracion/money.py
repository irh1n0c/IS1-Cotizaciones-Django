#!/usr/bin/python
# -*- coding: utf-8 -*-

from decimal import Decimal, ROUND_HALF_UP
from typing import Union


class Money:
    """Value Object que representa una cantidad monetaria."""
    
    def __init__(self, amount: Union[int, float, Decimal], currency: str = "USD"):
        if isinstance(amount, (int, float)):
            amount = Decimal(str(amount))
        elif not isinstance(amount, Decimal):
            raise ValueError("El monto debe ser un número")
        
        if amount < 0:
            raise ValueError("El monto no puede ser negativo")
        
        if not currency or not isinstance(currency, str):
            raise ValueError("La moneda debe ser una cadena válida")
        
        self._amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self._currency = currency.upper()
    
    @property
    def amount(self) -> Decimal:
        """Retorna el monto."""
        return self._amount
    
    @property
    def currency(self) -> str:
        """Retorna la moneda."""
        return self._currency
    
    def add(self, other: 'Money') -> 'Money':
        """Suma dos cantidades monetarias."""
        self._validate_same_currency(other)
        return Money(self._amount + other._amount, self._currency)
    
    def subtract(self, other: 'Money') -> 'Money':
        """Resta dos cantidades monetarias."""
        self._validate_same_currency(other)
        result_amount = self._amount - other._amount
        if result_amount < 0:
            raise ValueError("El resultado no puede ser negativo")
        return Money(result_amount, self._currency)
    
    def multiply(self, factor: Union[int, float, Decimal]) -> 'Money':
        """Multiplica la cantidad por un factor."""
        if isinstance(factor, (int, float)):
            factor = Decimal(str(factor))
        
        if factor < 0:
            raise ValueError("El factor no puede ser negativo")
        
        return Money(self._amount * factor, self._currency)
    
    def apply_discount(self, percentage: Union[int, float, Decimal]) -> 'Money':
        """Aplica un descuento porcentual."""
        if isinstance(percentage, (int, float)):
            percentage = Decimal(str(percentage))
        
        if percentage < 0 or percentage > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        
        discount_factor = Decimal('1') - (percentage / Decimal('100'))
        return Money(self._amount * discount_factor, self._currency)
    
    def apply_tax(self, tax_rate: Union[int, float, Decimal]) -> 'Money':
        """Aplica un impuesto."""
        if isinstance(tax_rate, (int, float)):
            tax_rate = Decimal(str(tax_rate))
        
        if tax_rate < 0:
            raise ValueError("La tasa de impuesto no puede ser negativa")
        
        tax_factor = Decimal('1') + (tax_rate / Decimal('100'))
        return Money(self._amount * tax_factor, self._currency)
    
    def _validate_same_currency(self, other: 'Money') -> None:
        """Valida que ambas cantidades tengan la misma moneda."""
        if self._currency != other._currency:
            raise ValueError(f"No se pueden operar monedas diferentes: {self._currency} vs {other._currency}")
    
    def is_zero(self) -> bool:
        """Indica si el monto es cero."""
        return self._amount == Decimal('0')
    
    def is_greater_than(self, other: 'Money') -> bool:
        """Compara si este monto es mayor que otro."""
        self._validate_same_currency(other)
        return self._amount > other._amount
    
    def is_less_than(self, other: 'Money') -> bool:
        """Compara si este monto es menor que otro."""
        self._validate_same_currency(other)
        return self._amount < other._amount
    
    def __str__(self) -> str:
        return f"{self._amount} {self._currency}"
    
    def __repr__(self) -> str:
        return f"Money({self._amount}, '{self._currency}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Money):
            return False
        return self._amount == other._amount and self._currency == other._currency
    
    def __hash__(self) -> int:
        return hash((self._amount, self._currency))
    
    @classmethod
    def zero(cls, currency: str = "USD") -> 'Money':
        """Crea una instancia con monto cero."""
        return cls(Decimal('0'), currency)
    
    @classmethod
    def from_string(cls, amount_str: str, currency: str = "USD") -> 'Money':
        """Crea una instancia desde un string."""
        try:
            amount = Decimal(amount_str)
            return cls(amount, currency)
        except (ValueError, TypeError):
            raise ValueError(f"No se puede convertir '{amount_str}' a Money")