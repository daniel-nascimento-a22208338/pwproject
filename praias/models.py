from django.db import models

class Regiao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Servico(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Praia(models.Model):
    nome = models.CharField(max_length=100)
    regiao = models.ForeignKey(Regiao, on_delete=models.CASCADE)
    servicos = models.ManyToManyField(Servico)
    descricao = models.TextField(blank=True)
    classificacao = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    imagem = models.ImageField(upload_to='praias/', blank=True, null=True)

    def __str__(self):
        return self.nome
