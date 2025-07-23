from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from datetime import datetime

# Cookbook: funciones utilitarias para usuario
def validar_email_unico(email):
    if Usuario.objects.filter(email=email).exists():
        raise ValidationError("El email ya está registrado.")

def generar_userid(email):
    # Receta para crear un userid único basado en el email y la fecha
    return f"{email.split('@')[0]}_{int(datetime.now().timestamp())}"

class UsuarioManager(BaseUserManager):
    def create_user(self, userid, password=None, **extra_fields):
        if not userid:
            raise ValueError("El campo 'userid' es obligatorio.")
        if not password:
            raise ValueError("La contraseña es obligatoria.")
        if 'email' not in extra_fields or not extra_fields['email']:
            raise ValueError("El email es obligatorio.")
        
        user = self.model(userid=userid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, userid, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(userid, password, **extra_fields)

class Usuario(AbstractBaseUser):
    # Persistent-Tables: modelo persistente en base de datos
    userid = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    loginstatus = models.CharField(max_length=20, default='offline')
    registerdate = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['email']

    objects = UsuarioManager()

    def __str__(self):
        return self.userid

    # DESPUÉS
    def verify_login(self, password):

        # Error/Exception Handling
        try:
            return self.check_password(password)
        except Exception:
            self.loginstatus = 'error'
            self.save()
            return False

    # Cookbook: receta para registrar acceso
    def registrar_acceso(self):
        # Aquí podrías guardar en una tabla de auditoría, enviar notificación, etc.
        pass

    # Lazy-Rivers: método que solo calcula el último acceso si se solicita
    @property
    def ultimo_acceso(self):
        # Simulación de acceso perezoso
        return self.registerdate
    
# NUEVO: LoginService
class LoginService:
    def __init__(self, usuario):
        self.usuario = usuario

    def login(self, password):
        if not self.usuario.check_password(password):
            self.usuario.loginstatus = 'failed'
            self.usuario.save()
            return False
        self.usuario.loginstatus = 'online'
        self.usuario.save()
        self.usuario.registrar_acceso()
        return True

# INTERFAZ
class UserIdGenerator:
    def generate(self, email):
        raise NotImplementedError
# IMPLEMENTACIÓN
class TimestampUserIdGenerator(UserIdGenerator):
    def generate(self, email):
        return f"{email.split('@')[0]}_{int(datetime.now().timestamp())}"


# INTERFAZ
class IUserRepository:
    def save(self, user): pass
    
# IMPLEMENTACIÓN
class DjangoUserRepository(IUserRepository):
    def save(self, user):
        user.save()
