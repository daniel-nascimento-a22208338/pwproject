# Generated by Django 4.0.6 on 2024-05-15 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0003_album_copies_sold_album_ratings_banda_premios_ganhos'),
    ]

    operations = [
        migrations.AddField(
            model_name='musica',
            name='biografia',
            field=models.TextField(default='', null=True),
        ),
    ]
