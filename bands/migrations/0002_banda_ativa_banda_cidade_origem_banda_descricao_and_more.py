# Generated by Django 4.0.6 on 2024-03-13 16:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banda',
            name='ativa',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='banda',
            name='cidade_origem',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='banda',
            name='descricao',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='banda',
            name='formada_em',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='banda',
            name='genero',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='banda',
            name='imagem',
            field=models.ImageField(default='band_default_image.jpg', upload_to=''),
        ),
        migrations.AddField(
            model_name='banda',
            name='website',
            field=models.URLField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='musica',
            name='link_Spotify',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='album',
            name='capa',
            field=models.ImageField(default='album_default_image.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='album',
            name='num_stars',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='album',
            name='release_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='banda',
            name='nome',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='integrante',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='integrante',
            name='dateOfBirth',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='integrante',
            name='firstName',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='integrante',
            name='instrument',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='integrante',
            name='lastName',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='musica',
            name='duracao',
            field=models.DurationField(default=''),
        ),
        migrations.AlterField(
            model_name='musica',
            name='genero',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='musica',
            name='lancamento',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='musica',
            name='letra',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='musica',
            name='nome',
            field=models.CharField(default='', max_length=100),
        ),
    ]
