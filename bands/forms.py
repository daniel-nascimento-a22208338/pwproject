from django import forms
from .models import Banda, Album, Musica

class BandaForm(forms.ModelForm):
    class Meta:
        model = Banda
        # Incluindo todos os campos que deseja tornar editáveis
        fields = '__all__'

class AlbumForm(forms.ModelForm):
   class Meta:
       model = Album
       fields = '__all__'  # Ou defina campos específicos

class MusicaForm(forms.ModelForm):
   class Meta:
       model = Musica
       fields = '__all__'  # Ou defina campos específicos

