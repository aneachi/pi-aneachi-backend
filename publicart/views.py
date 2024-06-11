from rest_framework import viewsets, status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            usuario = Usuario.objects.get(user=request.user)
            serializer = UsuarioSerializer(usuario, context={'request': request})
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "La contraseña antigua no es correcta."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"success": "La contraseña ha sido cambiada con éxito."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EstiloViewSet(viewsets.ModelViewSet):
    queryset = Estilo.objects.all()
    serializer_class = EstiloSerializer


class TecnicaViewSet(viewsets.ModelViewSet):
    queryset = Tecnica.objects.all()
    serializer_class = TecnicaSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        users = [usuario.user for usuario in queryset]
        user_serializer = UserSerializer(users, many=True)

        usuarios_data = serializer.data
        for usuario_data, user_data in zip(usuarios_data, user_serializer.data):
            usuario_data['user'] = user_data

        return Response(usuarios_data)

    def retrieve(self, request, *args, **kwargs):
        usuario = self.get_object()
        serializer = self.get_serializer(usuario)
        user = usuario.user

        user_serializer = UserSerializer(user)

        # Agregar el objeto User serializado al JSON del objeto Usuario
        usuario_data = serializer.data
        usuario_data['user'] = user_serializer.data

        return Response(usuario_data)

    def update(self, request, *args, **kwargs):
        usuario = self.get_object()
        user_data = request.data.pop('user', {})
        user = usuario.user
        try:
            user_serializer = UserSerializer(user, data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

            request.data['user'] = user.id

            serializer = self.get_serializer(usuario, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
        except Exception as e:
            print(e)

        return Response(serializer.data)

    def destroy(self, requet, *args, **kwargs):
        usuario = self.get_object()
        user = usuario.user
        self.perform_destroy(user)
        self.perform_destroy(usuario)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request
        })
        return context

    @action(detail=True, methods=['post'])
    def seguir(self, request, pk=None):
        usuario_a_seguir = self.get_object()
        usuario = Usuario.objects.get(user=request.user)
        if usuario.seguir(usuario_a_seguir.user):
            return Response({'status': 'usuario seguido'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'ya sigue a este usuario'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def dejar_de_seguir(self, request, pk=None):
        usuario_a_dejar_seguir = self.get_object()
        usuario = Usuario.objects.get(user=request.user)
        usuario.dejar_de_seguir(usuario_a_dejar_seguir.user)
        return Response({'status': 'usuario dejado de seguir'}, status=status.HTTP_200_OK)


class SeguimientoViewSet(viewsets.ModelViewSet):
    queryset = Seguimiento.objects.all()
    serializer_class = SeguimientoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['seguidor__id', 'seguido__id']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        seguidor = self.request.query_params.get('seguidor', None)
        seguido = self.request.query_params.get('seguido', None)
        if seguidor:
            queryset = queryset.filter(seguidor__id=seguidor)
        if seguido:
            queryset = queryset.filter(seguido__id=seguido)
        return queryset

class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        obra_data = request.data
        imagenes = request.FILES.getlist('imagenes')
        
        obra_serializer = self.get_serializer(data=obra_data)
        obra_serializer.is_valid(raise_exception=True)
        obra = obra_serializer.save()

        # Crear Publicacion
        user = request.user  # Obtener usuario de la sesión
        publicacion_data = {'obra': obra.id, 'usuario': user.id}
        publicacion_serializer = PublicacionSerializer(data=publicacion_data)
        if publicacion_serializer.is_valid():
            publicacion_serializer.save()
        else:
            transaction.set_rollback(True)
            return Response(publicacion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Guardar las imágenes
        for imagen in imagenes:
            foto_data = {'obra': obra.id, 'foto': imagen}
            foto_serializer = FotoSerializer(data=foto_data)
            if foto_serializer.is_valid():
                foto_serializer.save()
            else:
                transaction.set_rollback(True)
                return Response(foto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(obra_serializer.data)
        return Response(obra_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class FotoViewSet(viewsets.ModelViewSet):
    queryset = Foto.objects.all()
    serializer_class = FotoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['obra__id']


class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer
    filter_backends = [SearchFilter]
    search_fields = ['usuario__id']


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        publicacion_id = request.data.get('publicacion')
        publicacion = Publicacion.objects.get(id=publicacion_id)
        usuario = Usuario.objects.get(user=request.user)

        like, created = Like.objects.get_or_create(usuario=usuario, publicacion=publicacion)

        if not created:
            return Response({'detail': 'Ya le has dado like a esta publicación'}, status=status.HTTP_400_BAD_REQUEST)

        publicacion.likes += 1
        publicacion.save()

        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        publicacion = instance.publicacion

        instance.delete()

        publicacion.likes -= 1
        publicacion.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='check-like/(?P<publicacion_id>\d+)')
    def check_like(self, request, publicacion_id=None):
        usuario = Usuario.objects.get(user=request.user)
        try:
            like = Like.objects.get(usuario=usuario, publicacion_id=publicacion_id)
            return Response({'like': like.id}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'like': None}, status=status.HTTP_200_OK)


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    filter_backends = [SearchFilter]
    search_fields = ['usuario__id']


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    filter_backends = [SearchFilter]
    search_fields = ['publicacion__id']


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        datos_solicitud = request.data

        chat_existente = Chat.objects.filter(usuario1_id=datos_solicitud['usuario1'], usuario2_id=datos_solicitud['usuario2']).exists()
        chat_existente2 = Chat.objects.filter(usuario1_id=datos_solicitud['usuario2'], usuario2_id=datos_solicitud['usuario1']).exists()

        if chat_existente or chat_existente2:
            return Response({'error': 'Ya existe un chat entre estas dos personas.'}, status=400)
        else:
            return super().create(request, *args, **kwargs)
        
    def udpate(self, request, *args, **kwargs):
        datos_solicitud = request.data

        chat_existente = Chat.objects.filter(usuario1_id=datos_solicitud['usuario1'], usuario2_id=datos_solicitud['usuario2']).exists()
        chat_existente2 = Chat.objects.filter(usuario1_id=datos_solicitud['usuario2'], usuario2_id=datos_solicitud['usuario1']).exists()

        if chat_existente or chat_existente2:
            return Response({'error': 'Ya existe un chat entre estas dos personas.'}, status=400)
        else:
            return super().create(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        chat = self.get_object()
        messages = chat.conversacion_set.all()
        serializer = ConversacionSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        chat = self.get_object()
        autor_id = request.data.get('autor')
        contenido = request.data.get('contenido')

        autor = get_object_or_404(Usuario, pk=autor_id)
        conversacion = Conversacion(chat=chat, autor=autor, contenido=contenido)
        conversacion.save()

        serializer = ConversacionSerializer(conversacion)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def get_or_create_chat(self, request):
        usuario1_id = request.data.get('usuario1')
        usuario2_id = request.data.get('usuario2')
        
        usuario1 = get_object_or_404(Usuario, id=usuario1_id)
        usuario2 = get_object_or_404(Usuario, id=usuario2_id)
        
        chat = Chat.objects.filter(
            usuario1=usuario1, usuario2=usuario2
        ).first() or Chat.objects.filter(
            usuario1=usuario2, usuario2=usuario1
        ).first()
        
        if not chat:
            chat = Chat.objects.create(usuario1=usuario1, usuario2=usuario2)
        
        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ConversacionViewSet(viewsets.ModelViewSet):
    queryset = Conversacion.objects.all()
    serializer_class = ConversacionSerializer
    filter_backends = [SearchFilter]

    def get_queryset(self):
        queryset = Conversacion.objects.all()
        chat_id = self.request.query_params.get('chat_id', None)
        if chat_id is not None:
            queryset = queryset.filter(chat__id=chat_id)
            # Opcional: para filtrar también por el campo leído
            leido = self.request.query_params.get('leido', None)
            if leido is not None and leido.lower() == 'false':
                queryset = queryset.filter(leido=False)
        return queryset
