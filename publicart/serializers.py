from rest_framework import serializers
from drf_extra_fields.fields import HybridImageField
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La nueva contraseña debe tener al menos 8 caracteres.")
        return value


class EstiloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estilo
        fields = '__all__'


class TecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnica
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    foto_perfil = HybridImageField(
        max_length=None,
        required=True,
        allow_null=True,
        represent_in_base64=True
    )
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = '__all__'

    def get_is_followed(self, obj):
        user = self.context['request'].user
        return Seguimiento.objects.filter(seguidor=user, seguido=obj.user).exists()

    def get_seguidores(self, obj):
        return Seguimiento.objects.filter(seguido=obj.user).count()
    
    def get_seguidos(self, obj):
        return Seguimiento.objects.filter(seguidor=obj.user).count()


class RegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Usuario
        fields = ('user', 'dni')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        usuario = Usuario.objects.create(user=user, dni=validated_data['dni'])
        return usuario


class SeguimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguimiento
        fields = '__all__'


class ObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obra
        fields = '__all__'

class FotoSerializer(serializers.ModelSerializer):
    foto = HybridImageField(
        max_length=None,
        required=True,
        allow_null=False,
        represent_in_base64=True
    )

    class Meta:
        model = Foto
        fields = '__all__'


class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = '__all__'


class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ConversacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversacion
        fields = '__all__'