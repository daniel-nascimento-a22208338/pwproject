# Generated by Django 4.0.6 on 2024-04-23 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Regiao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Praia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True)),
                ('localizacao', models.CharField(blank=True, max_length=255)),
                ('classificacao', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='praias/')),
                ('regiao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='praias.regiao')),
                ('servicos', models.ManyToManyField(to='praias.servico')),
            ],
        ),
    ]