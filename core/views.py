from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario, generar_userid
from django.views import View

# Cookbook: función para obtener usuario por email
def obtener_usuario_por_email(email):
    try:
        return Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return None

# Pipeline + Error/Exception Handling: vista de registro
class RegistroUsuarioView(View):
    def get(self, request):
        return render(request, 'core/registro.html', {'tipo_usuario_choices': Usuario.TIPO_USUARIO_CHOICES})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        tipo_usuario = request.POST.get('tipo_usuario', 'CLIENTE')  # Por defecto cliente
        
        # Solo superusuarios pueden crear administradores
        if tipo_usuario == 'ADMIN' and not request.user.is_superuser:
            messages.error(request, "No tienes permisos para crear administradores.")
            return render(request, 'core/registro.html')
        
        userid = generar_userid(email)
        try:
            Usuario.objects.create_user(
                userid=userid, 
                email=email, 
                password=password,
                tipo_usuario=tipo_usuario
            )
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error en el registro: {e}")
            return render(request, 'core/registro.html')

# Pipeline + Error/Exception Handling: vista de login
class LoginUsuarioView(View):
    def get(self, request):
        return render(request, 'core/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = obtener_usuario_por_email(email)
        
        if user and user.login_pipeline(password):
            messages.success(request, "Login exitoso.")
            
            # Redirigir según tipo de usuario
            if user.tipo_usuario == 'ADMIN':
                return redirect('admin:index')  # Panel de administración
            else:
                return redirect('core:perfil', userid=user.userid)
        else:
            messages.error(request, "Credenciales incorrectas.")
            return render(request, 'core/login.html')

# Persistent-Tables: vista de perfil
def perfil_usuario(request, userid):
    user = Usuario.objects.get(userid=userid)
    return render(request, 'core/perfil.html', {'usuario': user})

def home(request):
    return render(request, 'core/home.html')
