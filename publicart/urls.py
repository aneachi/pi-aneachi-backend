from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'estilos', EstiloViewSet)
router.register(r'tecnicas', TecnicaViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'seguimiento', SeguimientoViewSet)
router.register(r'obras', ObraViewSet)
router.register(r'fotos', FotoViewSet)
router.register(r'publicaciones', PublicacionViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'compras', CompraViewSet)
router.register(r'comentarios', ComentarioViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'conversaciones', ConversacionViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('register/', RegisterView.as_view(), name='register'),
]