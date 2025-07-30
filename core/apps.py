from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

#detalles del equipo medico
class QuotationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cotizacion'
    verbose_name = 'Sistema de Cotizaciones'