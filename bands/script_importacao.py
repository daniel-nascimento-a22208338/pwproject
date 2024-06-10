import json
from django.utils import timezone
from bands.models import Banda, Integrante, Album

with open('bands/bandas.json') as f:
    bandas_data = json.load(f)
    for banda_data in bandas_data:
        integrantes_data = banda_data.pop('integrantes', [])
        banda, created = Banda.objects.get_or_create(nome=banda_data['nome'], defaults=banda_data)
        if created:
            for integrante_data in integrantes_data:
                # Converter a data de nascimento para um objeto de data
                date_of_birth = timezone.make_aware(timezone.datetime.combine(timezone.datetime.strptime(integrante_data['dateOfBirth'], '%Y-%m-%d').date(), timezone.datetime.min.time()))
                integrante_data['dateOfBirth'] = date_of_birth
                Integrante.objects.create(banda=banda, **integrante_data)

with open('bands/albums.json') as f:
    albuns_data = json.load(f)
    for album_data in albuns_data:
        artist_name = album_data.pop('artist')
        artist, _ = Banda.objects.get_or_create(nome=artist_name)
        # Converter a data de lançamento para um objeto de data
        release_date = timezone.make_aware(timezone.datetime.strptime(album_data['release_date'], '%Y-%m-%d'))
        album_data['release_date'] = release_date
        try:
            album = Album.objects.create(artist=artist, **album_data)
        except Exception as e:
            pass  # Se ocorrer um erro, simplesmente ignoramos e continuamos o loop
