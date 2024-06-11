from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


# Create your models here.
class Estilo(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name=_('Descripciones'))

    def __str__(self):
        return f"{self.descripcion}"

    class Meta:
        verbose_name_plural = _('Estilos')


class Tecnica(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name=_('Descripciones'))

    def __str__(self):
        return f"{self.descripcion}"

    class Meta:
        verbose_name_plural = _('Tecnicas')


class Usuario(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    dni = models.CharField(max_length=9, verbose_name=_('DNI'))
    foto_perfil = models.ImageField(upload_to='img/usu', max_length=250, blank=True, null=True, verbose_name=_('Foto de perfil'))
    direccion = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Direcciones'))
    biografia = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Biografías'))
    num_seguidores = models.PositiveIntegerField(default=0)
    num_seguidos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name_plural = _('Usuarios')

    def save(self, *args, **kwargs):
        if self.num_seguidores < 0:
            self.num_seguidores = 0
        if self.num_seguidos < 0:
            self.num_seguidos = 0
        super().save(*args, **kwargs)

    def seguir(self, user):
        if self.user == user:
            return False, 'No puedes seguirte a ti mismo.'
        seguimiento, created = Seguimiento.objects.get_or_create(seguidor=self.user, seguido=user)
        if created:
            user_profile = Usuario.objects.get(user=user)
            self.num_seguidos += 1
            user_profile.num_seguidores += 1
            self.save()
            user_profile.save()
        return created, 'Usuario seguido correctamente.' if created else 'Ya sigues a este usuario.'

    def dejar_de_seguir(self, usuario):
        usuario = Usuario.objects.get(user=usuario)
        result = Seguimiento.objects.filter(seguidor=self.user, seguido=usuario.user).delete()
        if result[0] > 0:
            self.num_seguidos -= 1
            usuario.num_seguidores -= 1
            self.save()
            usuario.save()


class Seguimiento(models.Model):
    seguidor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Seguidor'), related_name='seguidos')
    seguido = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Seguido'), related_name='seguidores')
    fecha_seguimiento = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de creación'))

    def __str__(self):
        return f"{self.seguidor} sigue a {self.seguido}"

    class Meta:
        verbose_name_plural = _('Seguimientos')
        unique_together = ('seguidor', 'seguido')


class Obra(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    descripcion = models.CharField(max_length=255, verbose_name=_('Descripción'))
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Precio'))
    disponible = models.BooleanField(default=False, validators=[MinValueValidator(0)], verbose_name=_('Disponible'))
    estilo = models.ForeignKey(Estilo, on_delete=models.PROTECT, verbose_name=_('Estilo'))
    tecnica = models.ForeignKey(Tecnica, on_delete=models.PROTECT, verbose_name=_('Tecnica'))

    def __str__(self):
        return f"{self.descripcion}"

    class Meta:
        verbose_name_plural = _('Obras')


class Foto(models.Model):
    foto = models.ImageField(upload_to='img/fotos', max_length=250, blank=True, null=True, verbose_name=_('Foto'))
    obra = models.ForeignKey(Obra, on_delete=models.PROTECT, verbose_name=_('Obras'))

    def __str__(self) -> str:
        return f"{self.foto}"
    
    class Meta:
        verbose_name_plural=_('Fotos')



class Publicacion(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.PROTECT, verbose_name=_('Obras'))
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, verbose_name=_('Usuarios'))
    fecha_publicacion = models.DateTimeField(default=timezone.now, verbose_name=_('Fechas Publicación'))
    likes = models.PositiveIntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.obra.descripcion} - {self.usuario.user.username}"
    
    class Meta:
        verbose_name_plural=_('Publicaciones')


class Like(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, verbose_name=_('Publicación'))
    fecha_like = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de like'))
    
    def __str__(self):
        return f"a {self.usuario} le ha gustado {self.publicacion}"
    
    class Meta:
        verbose_name_plural = _('Likes')


class Compra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, verbose_name=_('Usuarios'))
    obra = models.ForeignKey(Obra, on_delete=models.PROTECT, verbose_name=_('Obras'))
    fecha_compra = models.DateTimeField(default=timezone.now, verbose_name=_('Fechas Compra'))

    def __str__(self) -> str:
        return f"{self.obra.descripcion} - {self.usuario.user.username}"
    
    class Meta:
        verbose_name_plural=_('Compras')


class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, verbose_name=_('Usuarios'))
    publicacion = models.ForeignKey(Publicacion, on_delete=models.PROTECT, null=True, verbose_name=_('Publicación'))
    texto = models.CharField(max_length=500, verbose_name=_('Textos'))
    fecha = models.DateTimeField(default=timezone.now, verbose_name=_('Fechas'))

    def __str__(self) -> str:
        return f"{self.publicacion} - {self.usuario.user.username}"
    
    class Meta:
        verbose_name_plural=_('Comentarios')


class Chat(models.Model):
    usuario1 = models.ForeignKey(Usuario, on_delete=models.PROTECT, verbose_name=_('Usuarios'), related_name='chats1')
    usuario2 = models.ForeignKey(Usuario, on_delete=models.PROTECT, verbose_name=_('Usuarios'), related_name='chats2')
    
    def __str__(self) -> str:
        return f"{self.usuario1.user.username} - {self.usuario2.user.username}"
    
    class Meta:
        verbose_name_plural=_('Chats')
        

class Conversacion(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name=_('Chats'))
    autor = models.ForeignKey(Usuario, on_delete=models.PROTECT, verbose_name=_('Autores'))
    contenido = models.CharField(max_length=500, verbose_name=_('Contenidos'))
    fecha = models.DateTimeField(default=timezone.now, verbose_name=_('Fechas'))
    leido = models.BooleanField(default=False, verbose_name=_('Leído'))

    def __str__(self) -> str:
        return f"{self.autor.user.username}: {self.contenido}"
    
    class Meta:
        verbose_name_plural=_('Conversaciones')