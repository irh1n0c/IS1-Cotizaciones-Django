# ────────────── VISTAS USUARIO NORMAL (USUARIO DJANGO) ──────────────
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import PerfilCliente
from .forms import RegistroClienteForm

def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            PerfilCliente.objects.create(
                user=user,
                ruc_dni=form.cleaned_data['ruc'],
                direccion=form.cleaned_data['direccion'],
                telefono=form.cleaned_data['telefono']
            )
            login(request, user)
            return redirect('dashboard_cliente')
    else:
        form = RegistroClienteForm()
    return render(request, 'registro_cliente.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if hasattr(user, 'perfilcliente'):
                return redirect('dashboard_cliente')
            else:
                return redirect('dashboard_admin')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_cliente(request):
    if not hasattr(request.user, 'perfilcliente'):
        return redirect('dashboard_admin')
    return render(request, 'dashboard_cliente.html', {'usuario': request.user})

@login_required
def dashboard_admin(request):
    if hasattr(request.user, 'perfilcliente'):
        return redirect('dashboard_cliente')
    return render(request, 'dashboard_admin.html', {'usuario': request.user})


# ────────────── VISTAS USUARIO PERSONALIZADO (CLASE USUARIO) ──────────────
from django.contrib import messages
from django.views import View
from .models import Usuario, generar_userid

def obtener_usuario_por_email(email):
    try:
        return Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return None

class RegistroUsuarioView(View):
    def get(self, request):
        return render(request, 'core/registro.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        userid = generar_userid(email)
        try:
            Usuario.objects.create_user(userid=userid, email=email, password=password)
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error en el registro: {e}")
            return render(request, 'core/registro.html')

class LoginUsuarioView(View):
    def get(self, request):
        return render(request, 'core/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = obtener_usuario_por_email(email)
        if user and user.login_pipeline(password):
            messages.success(request, "Login exitoso.")
            return redirect('home')
        else:
            messages.error(request, "Credenciales incorrectas.")
            return render(request, 'core/login.html')

def perfil_usuario(request, userid):
    user = Usuario.objects.get(userid=userid)
    return render(request, 'core/perfil.html', {'usuario': user})

# Puedes dejar esta versión de home o combinarla con la otra
def home(request):
    return redirect('login')  # o render(request, 'core/home.html')
