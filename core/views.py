from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import PerfilCliente

from .forms import RegistroClienteForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


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
                ruc=form.cleaned_data['ruc'],
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

from django.shortcuts import redirect

def home(request):
    return redirect('login')  # o 'registro_cliente' si prefieres



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
