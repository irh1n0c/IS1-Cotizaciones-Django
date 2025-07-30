from core.cotizacion.domain.repositories.cotizacion_repository import CotizacionRepository
from core.cotizacion.domain.models.quotation import Quotation
from core.models import CotizacionModel  # Ajusta si tienes otro nombre

class CotizacionRepositoryImpl(CotizacionRepository):
    def guardar(self, cotizacion: Quotation):
        CotizacionModel.objects.create(
            num_quotation=cotizacion.num_quotation,
            client_id=cotizacion.client_id,
            description=cotizacion.description,
            date_added=cotizacion.date_added,
            date_created=cotizacion.date_created,
            date_deleted=cotizacion.date_deleted,
            marca=cotizacion.marca,
            numero_serie=cotizacion.numero_serie
        )
