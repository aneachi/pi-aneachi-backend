# Generated by Django 4.2.6 on 2024-06-07 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicart', '0016_remove_obra_likes_publicacion_likes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='leido',
            field=models.BooleanField(default=False, verbose_name='Leído'),
        ),
    ]
