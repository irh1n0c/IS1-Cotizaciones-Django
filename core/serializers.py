# core/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PerfilCliente

class RegistroClienteSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    ruc = serializers.CharField()
    direccion = serializers.CharField()
    telefono = serializers.CharField()

    # Validación para evitar duplicados
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("El nombre de usuario ya está en uso.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("El correo electrónico ya está en uso.")
        return value

    def validate_ruc(self, value):
        if PerfilCliente.objects.filter(ruc=value).exists():
            raise serializers.ValidationError("El RUC ya está registrado.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        perfil = PerfilCliente.objects.create(
            user=user,
            ruc=validated_data['ruc'],
            direccion=validated_data['direccion'],
            telefono=validated_data['telefono']
        )
        return perfil


class PerfilClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilCliente
        fields = ['ruc', 'direccion', 'telefono']
