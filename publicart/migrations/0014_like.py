# Generated by Django 4.2.6 on 2024-06-04 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publicart', '0013_alter_usuario_biografia_alter_usuario_direccion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_like', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de like')),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publicart.publicacion', verbose_name='Publicación')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name_plural': 'Likes',
            },
        ),
    ]