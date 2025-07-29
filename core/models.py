from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from datetime import datetime

# ────── MODELO DE PERFIL CLIENTE (USUARIO ESTÁNDAR DJANGO) ──────
class PerfilCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ruc_dni = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

# ────── FUNCIONES UTILITARIAS PARA USUARIO PERSONALIZADO ──────
def validar_email_unico(email):
    if Usuario.objects.filter(email=email).exists():
        raise ValidationError("El email ya está registrado.")

def generar_userid(email):
    return f"{email.split('@')[0]}_{int(datetime.now().timestamp())}"

# ────── MANAGER PERSONALIZADO ──────
class UsuarioManager(BaseUserManager):
    def create_user(self, userid, password=None, **extra_fields):
        validar_email_unico(extra_fields.get('email'))
        user = self.model(userid=userid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userid, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(userid, password, **extra_fields)

# ────── MODELO DE USUARIO PERSONALIZADO ──────
class Usuario(AbstractBaseUser):
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

    def login_pipeline(self, password):
        if not self.verifiLogin(password):
            self.loginstatus = 'failed'
            self.save()
            return False
        self.loginstatus = 'online'
        self.save()
        self.registrar_acceso()
        return True

    def verifiLogin(self, password):
        try:
            return self.check_password(password)
        except Exception:
            self.loginstatus = 'error'
            self.save()
            return False

    def registrar_acceso(self):
        pass

    @property
    def ultimo_acceso(self):
        return self.registerdate
