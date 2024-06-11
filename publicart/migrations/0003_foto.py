# Generated by Django 4.2.6 on 2024-04-23 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publicart', '0002_rename_fotoperfil_usuario_foto_perfil_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.CharField(max_length=255)),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='publicart.obra', verbose_name='Obras')),
            ],
            options={
                'verbose_name_plural': 'Fotos',
            },
        ),
    ]
