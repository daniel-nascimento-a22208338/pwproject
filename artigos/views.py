from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category, Autor, Leitor, Pessoa, Comment
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import ArticleForm
from .forms import CommentForm

@login_required
def criar_comentario_view(request, artigo_id):
    artigo = get_object_or_404(Article, id=artigo_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.article = artigo
            comentario.commenter = request.user.leitor  # Associe ao usuário atual
            comentario.save()
            return redirect('artigos:detalhes_artigo', artigo_id=artigo_id)
    else:
        form = CommentForm()
    return render(request, 'artigos/criar_comentario.html', {'form': form, 'artigo': artigo})

@login_required
def editar_comentario_view(request, comentario_id):
    comentario = get_object_or_404(Comment, id=comentario_id)
    if comentario.commenter != request.user.leitor:
        raise PermissionDenied  # Verifica se o usuário é o proprietário do comentário

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('artigos:detalhes_artigo', artigo_id=comentario.article.id)
    else:
        form = CommentForm(instance=comentario)
    return render(request, 'artigos/editar_comentario.html', {'form': form, 'comentario': comentario})

@login_required
def apagar_comentario_view(request, comentario_id):
    comentario = get_object_or_404(Comment, id=comentario_id)
    if comentario.commenter != request.user.leitor:
        raise PermissionDenied  # Verifica se o usuário é o proprietário do comentário

    if request.method == 'POST':
        artigo_id = comentario.article.id
        comentario.delete()
        return redirect('artigos:detalhes_artigo', artigo_id=artigo_id)
    return render(request, 'artigos/confirmar_apagar_comentario.html', {'comentario': comentario})

@login_required
def criar_artigo_view(request):
    if not request.user.has_perm('artigos.add_article'):
        raise PermissionDenied

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('artigos:artigos_list')
    else:
        form = ArticleForm()

    return render(request, 'artigos/criar_artigo.html', {'form': form})

@login_required
def editar_artigo_view(request, artigo_id):
    artigo = get_object_or_404(Article, id=artigo_id)
    if not request.user.has_perm('artigos.change_article'):
        raise PermissionDenied

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=artigo)
        if form.is_valid():
            form.save()
            return redirect('artigos:artigos_list')
    else:
        form = ArticleForm(instance=artigo)

    return render(request, 'artigos/editar_artigo.html', {'form': form, 'artigo': artigo})

@login_required
def apagar_artigo_view(request, artigo_id):
    artigo = get_object_or_404(Article, id=artigo_id)
    if not request.user.has_perm('artigos.delete_article'):
        raise PermissionDenied

    if request.method == 'POST':
        artigo.delete()
        return redirect('artigos:artigos_list')

    return render(request, 'artigos/confirmar_apagar_artigo.html', {'artigo': artigo})

class CustomLoginView(LoginView):
    template_name = 'artigos/login.html'
    redirect_authenticated_user = True  # Redirecionar se já estiver autenticado
    next_page = ''  # Substitua pela URL desejada

class CustomLogoutView(LogoutView):
    template_name = 'artigos/logout.html'

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('artigos:artigos_list')  # Altere para a página inicial ou desejada
    else:
        form = RegistroForm()
    return render(request, 'artigos/registro.html', {'form': form})


def artigos_list_view(request):
    artigos = Article.objects.all()

    # Verificar permissões se o usuário estiver autenticado
    pode_adicionar = request.user.is_authenticated and request.user.has_perm('artigos.add_article')
    pode_editar = request.user.is_authenticated and request.user.has_perm('artigos.change_article')
    pode_apagar = request.user.is_authenticated and request.user.has_perm('artigos.delete_article')

    contexto = {
        'artigos': artigos,
        'pode_adicionar': pode_adicionar,
        'pode_editar': pode_editar,
        'pode_apagar': pode_apagar,
    }

    return render(request, 'artigos/artigos_list.html', contexto)

def detalhes_artigo_view(request, artigo_id):
    artigo = get_object_or_404(Article, id=artigo_id)
    comentarios = Comment.objects.filter(article=artigo)
    return render(request, 'artigos/detalhes_artigo.html', {'artigo': artigo, 'comentarios': comentarios})

def detalhes_autor_view(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    return render(request, 'artigos/detalhes_autor.html', {'autor': autor})

def detalhes_leitor_view(request, leitor_id):
    leitor = get_object_or_404(Leitor, pk=leitor_id)
    return render(request, 'artigos/detalhes_leitor.html', {'leitor': leitor})