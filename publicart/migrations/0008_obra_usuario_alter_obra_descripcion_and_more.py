# Generated by Django 4.2.6 on 2024-05-08 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publicart', '0007_alter_comentario_fecha_alter_comentario_texto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='obra',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='publicart.usuario', verbose_name='Usuario'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='obra',
            name='descripcion',
            field=models.CharField(max_length=255, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='obra',
            name='disponible',
            field=models.BooleanField(default=False, verbose_name='Disponible'),
        ),
        migrations.AlterField(
            model_name='obra',
            name='estilo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='publicart.estilo', verbose_name='Estilo'),
        ),
        migrations.AlterField(
            model_name='obra',
            name='precio',
            field=models.PositiveIntegerField(verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='obra',
            name='tecnica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='publicart.tecnica', verbose_name='Tecnica'),
        ),
    ]
