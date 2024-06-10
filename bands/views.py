from django.shortcuts import render, get_object_or_404, redirect
from .models import Banda, Album, Musica
from django.contrib.auth import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from .forms import BandaForm
from .forms import AlbumForm
from .forms import MusicaForm


@login_required
def criar_musica_view(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if not request.user.has_perm('bands.add_musica'):
        raise PermissionDenied

    if request.method == 'POST':
        form = MusicaForm(request.POST)
        if form.is_valid():
            musica = form.save(commit=False)
            musica.album = album
            musica.save()
            return redirect('bands:detalhes_album', album.id)
    else:
        form = MusicaForm()

    return render(request, 'bands/criar_musica.html', {'form': form, 'album': album})

@login_required
def editar_musica_view(request, musica_id):
    musica = get_object_or_404(Musica, id=musica_id)
    album = musica.album
    if not request.user.has_perm('bands.change_musica'):
        raise PermissionDenied

    if request.method == 'POST':
        form = MusicaForm(request.POST, instance=musica)
        if form.is_valid():
            form.save()
            return redirect('bands:detalhes_album', album.id)
    else:
        form = MusicaForm(instance=musica)

    return render(request, 'bands/editar_musica.html', {'form': form, 'album': album})

@login_required
def apagar_musica_view(request, musica_id):
    musica = get_object_or_404(Musica, id=musica_id)
    album = musica.album
    if not request.user.has_perm('bands.delete_musica'):
        raise PermissionDenied

    if request.method == 'POST':
        musica.delete()
        return redirect('bands:detalhes_album', album.id)

    return render(request, 'bands/confirmar_apagar_musica.html', {'musica': musica, 'album': album})

@login_required
def criar_album_view(request):
    if not request.user.has_perm('bands.add_album'):
        raise PermissionDenied
    artist_id = request.GET.get('artist_id')  # Obtenha a banda pela qual o álbum será criado
    banda = get_object_or_404(Banda, id=artist_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.artist = banda  # Associe o álbum à banda
            album.save()
            return redirect('bands:detalhes_banda', banda.id)
    else:
        form = AlbumForm()
    return render(request, 'bands/criar_album.html', {'form': form, 'banda': banda})

@login_required
def editar_album_view(request, album_id):
    if not request.user.has_perm('bands.change_album'):
        raise PermissionDenied
    album = get_object_or_404(Album, id=album_id)
    banda = album.artist
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect('bands:detalhes_banda', banda.id)
    else:
        form = AlbumForm(instance=album)
    return render(request, 'bands/editar_album.html', {'form': form, 'banda': banda})

@login_required
def apagar_album_view(request, album_id):
    if not request.user.has_perm('bands.delete_album'):
        raise PermissionDenied
    album = get_object_or_404(Album, id=album_id)
    banda = album.artist
    if request.method == 'POST':
        album.delete()
        return redirect('bands:detalhes_banda', banda.id)
    return render(request, 'bands/confirmar_apagar_album.html', {'album': album, 'banda': banda})

@login_required
def adicionar_banda_view(request):
    if not request.user.has_perm('bands.add_banda'):
        raise PermissionDenied
    # Lógica para adicionar uma nova banda

@login_required
def editar_banda_view(request, banda_id):
    if not request.user.has_perm('bands.change_banda'):
        raise PermissionDenied
    # Lógica para editar uma banda existente

@login_required
def apagar_banda_view(request, banda_id):
    if not request.user.has_perm('bands.delete_banda'):
        raise PermissionDenied
    # Lógica para apagar uma banda existente


def bandas_list_view(request):
    bandas = Banda.objects.all()

    # Verificar permissões do usuário, se ele estiver autenticado
    pode_adicionar = request.user.has_perm('bands.add_banda') if request.user.is_authenticated else False
    pode_editar = request.user.has_perm('bands.change_banda') if request.user.is_authenticated else False
    pode_apagar = request.user.has_perm('bands.delete_banda') if request.user.is_authenticated else False

    # Contexto para o template
    contexto = {
        'bandas': bandas,
        'pode_adicionar': pode_adicionar,
        'pode_editar': pode_editar,
        'pode_apagar': pode_apagar
    }

    return render(request, 'bands/bandas_list.html', contexto)

def detalhes_banda_view(request, banda_id):
    banda = get_object_or_404(Banda, id=banda_id)
    albuns = Album.objects.filter(artist=banda)

    # Verificar permissões apenas se o usuário estiver autenticado
    pode_adicionar = request.user.is_authenticated and request.user.has_perm('bands.add_album')
    pode_editar = request.user.is_authenticated and request.user.has_perm('bands.change_album')
    pode_apagar = request.user.is_authenticated and request.user.has_perm('bands.delete_album')

    contexto = {
        'banda': banda,
        'albuns': albuns,
        'pode_adicionar': pode_adicionar,
        'pode_editar': pode_editar,
        'pode_apagar': pode_apagar,
    }

    return render(request, 'bands/banda.html', contexto)

def detalhes_album_view(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    musicas = Musica.objects.filter(album=album)

    # Verificar permissões
    pode_adicionar = request.user.is_authenticated and request.user.has_perm('bands.add_musica')
    pode_editar = request.user.is_authenticated and request.user.has_perm('bands.change_musica')
    pode_apagar = request.user.is_authenticated and request.user.has_perm('bands.delete_musica')

    contexto = {
        'album': album,
        'musicas': musicas,
        'pode_adicionar': pode_adicionar,
        'pode_editar': pode_editar,
        'pode_apagar': pode_apagar,
    }

    return render(request, 'bands/album.html', contexto)

def detalhes_musica_view(request, musica_id):
    musica = get_object_or_404(Musica, id=musica_id)
    return render(request, 'bands/musica.html', {'musica': musica})

def registo_view(request):
    if request.method == "POST":
        models.User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            first_name=request.POST['nome'],
            last_name=request.POST['apelido'],
            password=request.POST['password']
        )
        return redirect('bands:login')

    return render(request, 'bands/registro.html')

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('bands:bandas_list')  # Redirecionar para a página desejada após login
        else:
            return render(request, 'bands/login.html', {
                'mensagem': 'Credenciais inválidas'
            })

    return render(request, 'bands/login.html')

def logout_view(request):
    logout(request)
    return redirect('bands:bandas_list')

@login_required
@permission_required('bands.add_banda', raise_exception=True)
def criar_banda_view(request):
    if request.method == "POST":
        form = BandaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bands:bandas_list')  # Nome da URL para listar bandas
    else:
        form = BandaForm()
    return render(request, 'bands/criar_banda.html', {'form': form})

@login_required
@permission_required('bands.change_banda', raise_exception=True)
def editar_banda_view(request, banda_id):
    banda = get_object_or_404(Banda, id=banda_id)
    if request.method == "POST":
        form = BandaForm(request.POST, instance=banda)
        if form.is_valid():
            form.save()
            return redirect('bands:bandas_list')
    else:
        form = BandaForm(instance=banda)
    return render(request, 'bands/editar_banda.html', {'form': form, 'banda': banda})

@login_required
@permission_required('bands.delete_banda', raise_exception=True)
def apagar_banda_view(request, banda_id):
    banda = get_object_or_404(Banda, id=banda_id)
    if request.method == "POST":
        banda.delete()
        return redirect('bands:bandas_list')
    return render(request, 'bands/apagar_banda.html', {'banda': banda})