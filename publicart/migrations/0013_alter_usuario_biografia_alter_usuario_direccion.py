# Generated by Django 4.2.6 on 2024-05-31 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicart', '0012_alter_seguimiento_options_alter_seguimiento_seguido_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='biografia',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Biografías'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='direccion',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Direcciones'),
        ),
    ]
