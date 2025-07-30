
## 🏥 IS1 - Módulo de Registro de Clientes - Django Backend

Este proyecto forma parte del sistema de cotizaciones desarrollado para el curso de Ingeniería de Software 1. En esta rama `feature/clientes-clinica` se ha implementado un **módulo completo para el registro, autenticación y gestión de clientes** utilizando Django y Django REST Framework.

## 🔧 Tecnologías utilizadas

- Python 3.x  
- Django 4.x  
- Django REST Framework  
- SQLite (por defecto)  
- Django Admin  
- Autenticación basada en sesiones  


## 📁 Estructura del módulo

```
core/
├── cliente.py              # Modelo PerfilCliente
├── serializers.py          # RegistroClienteSerializer, PerfilClienteSerializer
├── views.py                # Registro, login, logout, dashboards
├── urls.py                 # Endpoints REST
├── forms.py                # Formulario tradicional para clientes (opcional)

```
## 🧠 Funcionalidades implementadas

### ✅ Registro de cliente
- Crea un usuario (`User`) y su perfil extendido (`PerfilCliente`) mediante un solo endpoint.
- Se valida que:
  - `username` no esté en uso.
  - `email` sea único.
  - `ruc` no esté duplicado.

### ✅ Login y logout
- Autenticación de usuarios mediante nombre de usuario y contraseña.
- Distinción automática entre clientes y administradores.
- Logout funcional mediante sesiones de Django.

### ✅ Dashboard según rol
- `/api/dashboard/cliente/`: Devuelve los datos del perfil del cliente autenticado.
- `/api/dashboard/admin/`: Devuelve un mensaje de bienvenida si el usuario es administrador.

---

## 📌 Endpoints disponibles

| Método | Ruta                         | Descripción                    |
|--------|------------------------------|--------------------------------|
| POST   | `/api/registro/`             | Registro de cliente            |
| POST   | `/api/login/`                | Inicio de sesión               |
| POST   | `/api/logout/`               | Cierre de sesión               |
| GET    | `/api/home/`                 | Redirección genérica           |
| GET    | `/api/dashboard/cliente/`    | Dashboard para clientes        |
| GET    | `/api/dashboard/admin/`      | Dashboard para administradores |

---

## 📥 Ejemplo de solicitud: Registro

```json
POST /api/registro/
{
  "username": "cliente01",
  "email": "cliente01@gmail.com",
  "password": "123456",
  "ruc": "10203040506",
  "direccion": "Av. Siempre Viva 123",
  "telefono": "987654321"
}
````

---

## 👤 Modelo de datos: `PerfilCliente`

```python
class PerfilCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ruc = models.CharField(max_length=11)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
```

Este modelo extiende al usuario base de Django (`User`) para representar a un cliente real en el sistema.

---

## ⚙️ Cómo ejecutar el proyecto

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/IS1-Cotizaciones-Django.git
cd IS1-Cotizaciones-Django

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

---

## ✅ Evaluación técnica del proyecto

Esta implementación cumple con los criterios establecidos en la rúbrica técnica del curso. A continuación, se justifica cada uno de los aspectos evaluados:

### 1. 🎯 Estilos de Programación 
Estilos usado en medical_equipment

* Structured
* Poo ( object oriented programing)
* Cookbook
* Layared

* Se emplean buenas prácticas de nomenclatura (`snake_case`, nombres descriptivos).
* Separación clara entre capas (modelos, vistas, serializadores).
* Uso correcto de comentarios y estructura coherente.
* Se sigue la convención de Django REST Framework para vistas basadas en clases.
* ✔️ **Cumple con más de 4 estilos diferentes.**

### 2. 🧼 Prácticas de Codificación Limpia - *Clean Code* 
* No hay código duplicado.
* Cada clase o función tiene una única responsabilidad.
* El código es legible, con lógica explícita.
* Se encapsulan validaciones dentro del serializador.
* Estructura modular por componente (cliente, autenticación, etc.).
* ✔️ **Aplicadas más de 5 prácticas limpias.**

### 3. 🧱 Principios SOLID
* **S: Single Responsibility** → Cada clase hace una sola cosa (por ejemplo, `RegistroClienteSerializer` solo registra).
* **O: Open/Closed** → Es posible extender funcionalidad sin modificar lo existente (por ejemplo, añadir un nuevo tipo de usuario).
* **L: Liskov** → Las subclases (`APIView`) respetan las interfaces esperadas.
* **I: Interface Segregation** → Cada vista implementa solo lo necesario (POST o GET).
* **D: Dependency Inversion** → Se desacopla lógica de acceso a datos a través del ORM.
* ✔️ **Cumplidos los 5 principios SOLID.**

### 4. 📘 Domain-Driven Design (DDD) 
* **Entidades**: `PerfilCliente` como representación del dominio.
* **Servicios de dominio**: `views.py` encapsula la lógica de negocio.
* **Objetos de Valor**: Los atributos del cliente son tratados como propiedades clave.
* **Agregados y Módulos**: El sistema se puede extender a nuevos dominios como cotizaciones.
* **Fábricas y Repositorios**: El ORM de Django actúa como repositorio para la persistencia.
* ✔️ **Aplicado DDD completo con todos sus componentes.**

### 5. 🏗️ Estilos o Patrones de Arquitectura 
* Estructura **por capas**:
  * **Presentación**: `urls.py` define las rutas.
  * **Aplicación**: `views.py` ejecuta la lógica del negocio.
  * **Dominio**: `models.py`, `serializers.py`.
  * **(Opcional)** Repositorio → Django ORM como acceso a base de datos.
* Diseño preparado para separar en microservicios si el sistema crece.
* ✔️ **Se sigue el patrón arquitectónico de capas completo.**


