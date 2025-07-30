from abc import ABC, abstractmethod
from core.cotizacion.domain.models.quotation import Quotation


class CotizacionRepository(ABC):
    @abstractmethod
    def guardar(self, cotizacion: Quotation):
        """Guarda una cotización en el sistema"""
        pass
