# Guía de Instalación y Ejecución - Sistema de Cotizaciones DDD

## 🚀 Cómo Ejecutar la Aplicación Localmente

### Prerrequisitos

- **Python 3.11.9** o superior
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)

### 1. Preparación del Entorno

#### Verificar Python
```bash
python --version
# Debe mostrar: Python 3.11.9 o superior
```

#### Crear entorno virtual (recomendado)
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 2. Instalación de Dependencias

```bash
# Instalar Django
pip install django==5.2.4

# Instalar dependencias adicionales para DDD
pip install python-dateutil
pip install typing-extensions
```

### 3. Configuración de la Base de Datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser
```

### 4. Inicialización DDD

Agrega esta configuración a tu `cotizaciones/settings.py`:

```python
# Al final del archivo settings.py
# Configuración DDD
DDD_ENABLE_NOTIFICATIONS = True
DDD_ENABLE_AUDIT = True
DDD_ENABLE_METRICS = True

# Inicializar DDD al arrancar Django
def setup_ddd():
    try:
        from core.dominio.Servicio_calibracion.ddd_config import setup_django_ddd
        setup_django_ddd()
        print("✅ DDD Configuration initialized successfully")
    except Exception as e:
        print(f"⚠️ DDD Configuration warning: {e}")

# Llamar setup al importar settings
setup_ddd()
```

### 5. Ejecutar la Aplicación

```bash
# Ejecutar servidor de desarrollo
python manage.py runserver

# La aplicación estará disponible en:
# http://localhost:8000/
```

### 6. Verificar la Instalación

#### Acceder a la aplicación:
- **Aplicación principal**: http://localhost:8000/
- **Panel de administración**: http://localhost:8000/admin/ (si creaste superusuario)

#### Verificar logs DDD:
Al iniciar el servidor, deberías ver:
```
✅ DDD Configuration initialized successfully
[NOTIFICATION] Sistema de notificaciones activo
[AUDIT] Sistema de auditoría activo
[METRICS] Sistema de métricas activo
```

## 🧪 Probar la Nueva Arquitectura DDD

### Endpoints Disponibles

#### **Para Empresas (CRUD Completo)**
```bash
# Crear cotización
POST /api/cotizaciones/
{
    "cliente_id": "cliente-123",
    "equipos": [
        {
            "name": "Monitor Cardíaco",
            "brand": "Philips",
            "model": "MX450",
            "price": 1500.00,
            "serial_number": "PHI-001"
        }
    ]
}

# Obtener cotizaciones de la empresa
GET /api/cotizaciones/

# Enviar cotización
PUT /api/cotizaciones/{id}/
{
    "action": "enviar"
}
```

#### **Para Clientes (Solo Lectura y Respuesta)**
```bash
# Ver cotizaciones asignadas
GET /api/cotizaciones/

# Aprobar cotización
PUT /api/cotizaciones/{id}/
{
    "action": "aprobar"
}

# Rechazar cotización
PUT /api/cotizaciones/{id}/
{
    "action": "rechazar",
    "motivo": "Precio muy alto"
}
```

### Probar Domain Events

Al realizar operaciones, verás logs automáticos:
```
[NOTIFICATION] Cotización C2025001 enviada a cliente cliente-123
[AUDIT] 2025-01-30T10:30:00: CotizacionEnviada - {...}
[METRICS] Counter cotizaciones_enviadas incremented
```

## 🔧 Configuración Avanzada

### Variables de Entorno (Opcional)

Crea un archivo `.env` en la raíz del proyecto:
```env
# Configuración DDD
DDD_ENABLE_NOTIFICATIONS=true
DDD_ENABLE_AUDIT=true
DDD_ENABLE_METRICS=true

# Configuración Django
DEBUG=true
SECRET_KEY=tu-secret-key-aqui
```

### Configuración de Logging

Agrega a `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'ddd': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
# Asegúrate de estar en el directorio correcto
cd d:/cs/IS1/Lab\ 9/IS1-Cotizaciones-Django

# Verificar estructura de archivos
ls -la core/dominio/Servicio_calibracion/
```

### Error: "No module named 'core'"
```bash
# Agregar el directorio actual al PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# En Windows:
set PYTHONPATH=%PYTHONPATH%;%cd%
```

### Error de Importación DDD
```bash
# Verificar que todos los archivos DDD existen
ls core/dominio/Servicio_calibracion/money.py
ls core/dominio/Servicio_calibracion/domain_events.py
ls core/servicios/repositories.py
```

### Base de Datos Corrupta
```bash
# Eliminar base de datos y recrear
rm db.sqlite3
python manage.py migrate
```

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real
```bash
# Ejecutar con logs detallados
python manage.py runserver --verbosity=2

# Ver solo logs DDD
python manage.py runserver 2>&1 | grep -E "\[NOTIFICATION\]|\[AUDIT\]|\[METRICS\]"
```

### Verificar Estado DDD
```python
# En shell de Django
python manage.py shell

>>> from core.dominio.Servicio_calibracion.ddd_config import get_ddd_config
>>> config = get_ddd_config()
>>> print(f"DDD Initialized: {config._initialized}")
>>> print(f"Event Handlers: {len(config._domain_event_dispatcher._handlers)}")
```

## 🚀 Despliegue en Producción

### Configuración para Producción
```python
# En settings.py para producción
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']

# Configuración DDD para producción
DDD_ENABLE_NOTIFICATIONS = True
DDD_ENABLE_AUDIT = True
DDD_ENABLE_METRICS = True
```

### Comandos de Despliegue
```bash
# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar con Gunicorn
pip install gunicorn
gunicorn cotizaciones.wsgi:application
```

## 📚 Recursos Adicionales

- **Documentación DDD**: [`DDD_IMPLEMENTATION.md`](DDD_IMPLEMENTATION.md)
- **Arquitectura**: Ver diagramas en la documentación
- **Ejemplos de Uso**: Revisar tests en los archivos de dominio

## ✅ Checklist de Verificación

- [ ] Python 3.11.9+ instalado
- [ ] Django 5.2.4 instalado
- [ ] Base de datos migrada
- [ ] Servidor ejecutándose en http://localhost:8000
- [ ] Logs DDD aparecen al iniciar
- [ ] Endpoints responden correctamente
- [ ] Domain Events funcionan

¡Tu aplicación Django con arquitectura DDD está lista para usar! 🎉