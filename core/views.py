# ────────────── IMPORTACIONES VISTAS ──────────────
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import PerfilCliente, Usuario, generar_userid
from .serializers import RegistroClienteSerializer, PerfilClienteSerializer
from .forms import RegistroClienteForm

"""code josel"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from core.cotizacion.domain.models.equipment_details import MedicalEquipment, MedicalEquipmentManager
from .forms import MedicalEquipmentForm, MedicalEquipmentSearchForm
from decimal import Decimal
# ────────────── VISTAS API REST ──────────────

class RegistroClienteAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegistroClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registro exitoso'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if hasattr(user, 'perfilcliente'):
                return Response({'message': 'Login exitoso', 'rol': 'cliente'})
            else:
                return Response({'message': 'Login exitoso', 'rol': 'admin'})
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Sesión cerrada correctamente'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def home_api(request):
    return Response({'message': 'Redirige a login'}, status=status.HTTP_302_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_cliente_api(request):
    if not hasattr(request.user, 'perfilcliente'):
        return Response({'error': 'No autorizado como cliente'}, status=status.HTTP_403_FORBIDDEN)
    
    perfil = PerfilCliente.objects.get(user=request.user)
    serializer = PerfilClienteSerializer(perfil)
    return Response({'perfil': serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_admin_api(request):
    if hasattr(request.user, 'perfilcliente'):
        return Response({'error': 'No autorizado como admin'}, status=status.HTTP_403_FORBIDDEN)
    return Response({'message': f'Bienvenido, {request.user.username} (admin)'})


# ────────────── VISTAS BASADAS EN HTML Y FORMULARIOS ──────────────

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
            return redirect('dashboard_cliente')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_cliente(request):
    if not hasattr(request.user, 'perfilcliente'):
        return redirect('login')
    perfil = PerfilCliente.objects.get(user=request.user)
    return render(request, 'dashboard_cliente.html', {'perfil': perfil})


# ────────────── VISTAS PERSONALIZADAS DE USUARIO (Clase Usuario) ──────────────

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

def home(request):
    return redirect('login')  # o render(request, 'core/home.html')


# ────────────── medical equipment ──────────────

def medical_equipment_list(request):
    """Vista para listar equipos médicos con búsqueda."""
    search_form = MedicalEquipmentSearchForm(request.GET or None)
    equipments = MedicalEquipmentManager.get_all_equipment()
    
    if search_form.is_valid():
        name = search_form.cleaned_data.get('name')
        brand = search_form.cleaned_data.get('brand')
        min_price = search_form.cleaned_data.get('min_price')
        max_price = search_form.cleaned_data.get('max_price')
        
        if name:
            equipments = MedicalEquipmentManager.find_by_name(name)
        elif brand:
            equipments = MedicalEquipmentManager.find_by_brand(brand)
        elif min_price and max_price:
            equipments = MedicalEquipmentManager.find_by_price_range(min_price, max_price)
    
    # Paginación
    paginator = Paginator(equipments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_count': len(equipments)
    }
    return render(request, 'medical_equipment/list.html', context)

def medical_equipment_create(request):
    """Vista para crear un nuevo equipo médico."""
    if request.method == 'POST':
        form = MedicalEquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            messages.success(request, f'Equipo "{equipment.name}" creado exitosamente.')
            return redirect('medical_equipment_detail', pk=equipment.id)
    else:
        form = MedicalEquipmentForm()
    
    return render(request, 'medical_equipment/create.html', {'form': form})

def medical_equipment_detail(request, pk):
    """Vista para mostrar detalles de un equipo médico."""
    equipment = get_object_or_404(MedicalEquipment, pk=pk)
    return render(request, 'medical_equipment/detail.html', {'equipment': equipment})

def medical_equipment_update(request, pk):
    """Vista para actualizar un equipo médico."""
    equipment = get_object_or_404(MedicalEquipment, pk=pk)
    
    if request.method == 'POST':
        form = MedicalEquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            equipment = form.save()
            messages.success(request, f'Equipo "{equipment.name}" actualizado exitosamente.')
            return redirect('medical_equipment_detail', pk=equipment.id)
    else:
        form = MedicalEquipmentForm(instance=equipment)
    
    return render(request, 'medical_equipment/update.html', {
        'form': form,
        'equipment': equipment
    })

@require_http_methods(["DELETE"])
def medical_equipment_delete(request, pk):
    """Vista para eliminar un equipo médico (AJAX)."""
    success = MedicalEquipmentManager.delete_equipment(pk)
    
    if success:
        return JsonResponse({'success': True, 'message': 'Equipo eliminado exitosamente.'})
    else:
        return JsonResponse({'success': False, 'message': 'Equipo no encontrado.'})