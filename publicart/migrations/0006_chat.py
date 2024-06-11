# Generated by Django 4.2.6 on 2024-04-23 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publicart', '0005_alter_compra_options_comentario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chats1', to='publicart.usuario', verbose_name='Usuarios')),
                ('usuario2', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='chats2', to='publicart.usuario', verbose_name='Usuarios')),
            ],
            options={
                'verbose_name_plural': 'Chats',
            },
        ),
    ]
