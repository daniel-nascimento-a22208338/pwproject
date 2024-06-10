from django.contrib import admin
from .models import Integrante, Banda, Album, Musica
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

class IntegranteAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'age', 'instrument', 'dateOfBirth')
    search_fields = ('firstName', 'lastName', 'instrument')

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'release_date', 'num_stars')
    search_fields = ('name', 'artist__nome')  # Permitindo pesquisa pelo nome do álbum e nome da banda/artista
    list_filter = ('artist', 'release_date')

class MusicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'album', 'genero', 'lancamento')
    search_fields = ('nome', 'album__name', 'genero')  # Permitindo pesquisa pelo nome da música, nome do álbum e gênero
    list_filter = ('album__artist', 'genero', 'lancamento')

# Register your models here.

class BandaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'genero', 'formada_em', 'cidade_origem', 'ativa', 'premios_ganhos')
    list_filter = ('genero', 'ativa')
    search_fields = ('nome', 'genero', 'cidade_origem')
    ordering = ('-premios_ganhos',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        top_option = request.GET.get('top')
        num_results = int(request.GET.get('num_results', 10))  # Valor padrão é 10

        if top_option == 'true':
            return queryset[:num_results]  # Retorna os 'num_results' primeiros artistas mais premiados
        elif top_option == 'false':
            return queryset.order_by('premios_ganhos')[:num_results]  # Retorna os 'num_results' últimos artistas menos premiados
        else:
            return queryset

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return list_display + ('top_option', 'num_results')

    def top_option(self, obj):
        return mark_safe(f'<a href="?{obj.id}&top=true&num_results={obj.id}">{_("Top Artists")}</a> | <a href="?{obj.id}&top=false&num_results={obj.id}">{_("Bottom Artists")}</a>')
    top_option.short_description = _('Top/Bottom Option')

    def num_results(self, obj):
        return mark_safe('<input type="number" min="1" name="num_results" value="10">')
    num_results.short_description = _('Number of Results')

admin.site.register(Integrante, IntegranteAdmin)
admin.site.register(Banda, BandaAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Musica, MusicaAdmin)
