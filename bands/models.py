from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils import timezone

class Integrante(models.Model):
    firstName = models.CharField(max_length=30, default='')
    lastName = models.CharField(max_length=50, default='')
    age = models.IntegerField(default=0)
    dateOfBirth = models.DateField(default=timezone.now)
    instrument = models.CharField(max_length=100, default='')

    def save(self, *args, **kwargs):
        # Calcula a idade com base na data de nascimento e a define no campo 'age'
        if self.dateOfBirth:
            today = timezone.now().date()
            age = today.year - self.dateOfBirth.year - ((today.month, today.day) < (self.dateOfBirth.month, self.dateOfBirth.day))
            self.age = age
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.firstName} {self.lastName} - {self.age} anos'


class Banda(models.Model):
    integrantes = models.ManyToManyField(Integrante)
    nome = models.CharField(max_length=100, default='')
    genero = models.CharField(max_length=50, default='')
    formada_em = models.DateField(default=now)
    cidade_origem = models.CharField(max_length=100, null=True, default='')
    descricao = models.TextField(default='')
    imagem = models.ImageField(default='band_default_image.jpg')
    website = models.URLField(null=True, blank=True, default='')
    ativa = models.BooleanField(default=True)
    premios_ganhos = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Album(models.Model):
    artist = models.ForeignKey(Banda, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    release_date = models.DateField(default=now)
    num_stars = models.IntegerField(default=0)
    capa = models.ImageField(default='album_default_image.jpg')
    ratings = models.FloatField(default=0.0)
    copies_sold = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} - released in {self.release_date}'

class Musica(models.Model):
    nome = models.CharField(max_length=100, default='')
    duracao = models.DurationField(default='')
    featuring = models.ManyToManyField(Banda, related_name='featuring', blank=True)
    album = models.ForeignKey('Album', on_delete=models.CASCADE, null=True)
    genero = models.CharField(max_length=50, null=True, blank=True, default='')
    biografia=models.TextField(default='', null=True)
    letra = models.TextField(null=True, blank=True, default='')
    lancamento = models.DateField(null=True, blank=True, default=now)
    link_Spotify = models.URLField(default='')

    def __str__(self):
        return self.nome

@receiver(post_save, sender=Album)
def update_banda_premios_ganhos(sender, instance, created, **kwargs):
    if created:
        instance.artist.premios_ganhos += instance.num_stars
        instance.artist.save()

