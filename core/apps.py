from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Sistema de Cotizaciones DDD'

    def ready(self):
        """
        Se ejecuta cuando Django ha cargado completamente la aplicación.
        Es el lugar correcto para inicializar la configuración DDD.
        """
        try:
            from core.dominio.Servicio_calibracion.ddd_config import setup_django_ddd
            setup_django_ddd()
            print("[OK] DDD Configuration initialized successfully")
            print("[INFO] Domain Events: Enabled")
            print("[INFO] Notifications: Enabled")
            print("[INFO] Audit: Enabled")
            print("[INFO] Metrics: Enabled")
        except ImportError as e:
            print(f"[WARNING] DDD modules not found: {e}")
            print("[INFO] DDD components will be available but not auto-configured")
        except Exception as e:
            print(f"[WARNING] DDD Configuration warning: {e}")
            print("[INFO] DDD will initialize on first use")
