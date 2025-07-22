# core/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import PerfilCliente
from .serializers import RegistroClienteSerializer, PerfilClienteSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# REGISTRO DE USUARIO + PERFIL CLIENTE
class RegistroClienteAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegistroClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registro exitoso'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LOGIN API
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


# LOGOUT API
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Sesión cerrada correctamente'}, status=status.HTTP_200_OK)


# HOME REDIRECT
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def home_api(request):
    return Response({'message': 'Redirige a login'}, status=status.HTTP_302_FOUND)


# DASHBOARD CLIENTE API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_cliente_api(request):
    if not hasattr(request.user, 'perfilcliente'):
        return Response({'error': 'No autorizado como cliente'}, status=status.HTTP_403_FORBIDDEN)
    
    perfil = PerfilCliente.objects.get(user=request.user)
    serializer = PerfilClienteSerializer(perfil)
    return Response({'perfil': serializer.data})


# DASHBOARD ADMIN API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_admin_api(request):
    if hasattr(request.user, 'perfilcliente'):
        return Response({'error': 'No autorizado como admin'}, status=status.HTTP_403_FORBIDDEN)
    
    return Response({'message': f'Bienvenido, {request.user.username} (admin)'})
