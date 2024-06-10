# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Curso, Disciplina, Projeto
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import CursoForm
from .forms import DisciplinaForm
from .forms import ProjetoForm

@login_required
def criar_projeto_view(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    if not request.user.has_perm('curso.add_projeto'):
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjetoForm(request.POST, request.FILES)
        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.disciplina = disciplina
            projeto.save()
            return redirect('curso:disciplina_detail', disciplina_id=disciplina.id)
    else:
        form = ProjetoForm()
    return render(request, 'curso/criar_projeto.html', {'form': form, 'disciplina': disciplina})

@login_required
def editar_projeto_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if not request.user.has_perm('curso.change_projeto'):
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjetoForm(request.POST, request.FILES, instance=projeto)
        if form.is_valid():
            form.save()
            return redirect('curso:disciplina_detail', disciplina_id=projeto.disciplina.id)
    else:
        form = ProjetoForm(instance=projeto)
    return render(request, 'curso/editar_projeto.html', {'form': form, 'projeto': projeto})

@login_required
def apagar_projeto_view(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)
    if not request.user.has_perm('curso.delete_projeto'):
        raise PermissionDenied

    if request.method == 'POST':
        disciplina_id = projeto.disciplina.id
        projeto.delete()
        return redirect('curso:disciplina_detail', disciplina_id=disciplina_id)
    return render(request, 'curso/confirmar_apagar_projeto.html', {'projeto': projeto})


@login_required
def criar_disciplina_view(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if not request.user.has_perm('curso.add_disciplina'):
        raise PermissionDenied

    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            disciplina = form.save(commit=False)
            disciplina.curso = curso
            disciplina.save()
            return redirect('curso:curso_detail', curso_id=curso.id)
    else:
        form = DisciplinaForm()
    return render(request, 'curso/criar_disciplina.html', {'form': form, 'curso': curso})

def editar_disciplina_view(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            cursos_associados = disciplina.cursos.all()
            if cursos_associados.exists():
                curso_id = cursos_associados[0].id  # Primeiro curso associado
                return redirect('curso:curso_detail', curso_id=curso_id)
            else:
                return redirect('curso:cursos')
    else:
        form = DisciplinaForm(instance=disciplina)

    # Adicionar o primeiro curso ao contexto (se houver)
    primeiro_curso = disciplina.cursos.first()  # Retorna o primeiro curso ou None se não houver cursos

    return render(request, 'curso/editar_disciplina.html', {'form': form, 'disciplina': disciplina, 'primeiro_curso': primeiro_curso})

@login_required
def apagar_disciplina_view(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    if not request.user.has_perm('curso.delete_disciplina'):
        raise PermissionDenied

    if request.method == 'POST':
        curso_id = disciplina.curso.id
        disciplina.delete()
        return redirect('curso:curso_detail', curso_id=curso_id)
    return render(request, 'curso/confirmar_apagar_disciplina.html', {'disciplina': disciplina})

@login_required
def criar_curso_view(request):
    if not request.user.has_perm('curso.add_curso'):
        raise PermissionDenied

    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('curso:cursos')
    else:
        form = CursoForm()
    return render(request, 'curso/criar_curso.html', {'form': form})

@login_required
def editar_curso_view(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if not request.user.has_perm('curso.change_curso'):
        raise PermissionDenied

    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('curso:cursos')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'curso/editar_curso.html', {'form': form, 'curso': curso})

@login_required
def apagar_curso_view(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    if not request.user.has_perm('curso.delete_curso'):
        raise PermissionDenied

    if request.method == 'POST':
        curso.delete()
        return redirect('curso:cursos')
    return render(request, 'curso/confirmar_apagar_curso.html', {'curso': curso})
class CustomLoginView(LoginView):
    template_name = 'curso/login.html'
    redirect_authenticated_user = True  # Redirecionar usuários já autenticados
    next_page = '/curso/'

class CursoLogoutView(LogoutView):
    # Template é opcional, o redirecionamento pode ser feito diretamente
    template_name = 'curso/logout.html'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('curso:cursos')

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Login automático após o registro
            return redirect('curso:cursos')  # Redireciona para a página padrão de cursos
    else:
        form = RegistroForm()
    return render(request, 'curso/registro.html', {'form': form})

def curso_detail(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    # Inicializar permissões como False
    pode_adicionar = False
    pode_editar = False
    pode_apagar = False

    if request.user.is_authenticated:
        pode_adicionar = request.user.has_perm('curso.add_disciplina')
        pode_editar = request.user.has_perm('curso.change_disciplina')
        pode_apagar = request.user.has_perm('curso.delete_disciplina')

    contexto = {
        'curso': curso,
        'pode_adicionar': pode_adicionar,
        'pode_editar': pode_editar,
        'pode_apagar': pode_apagar
    }

    return render(request, 'curso/curso_detail.html', contexto)

def disciplina_detail(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)

    pode_adicionar_projeto = False
    pode_editar_projeto = False
    pode_apagar_projeto = False

    if request.user.is_authenticated:
        pode_adicionar_projeto = request.user.has_perm('curso.add_projeto')
        pode_editar_projeto = request.user.has_perm('curso.change_projeto')
        pode_apagar_projeto = request.user.has_perm('curso.delete_projeto')

    return render(request, 'curso/disciplina_detail.html', {
        'disciplina': disciplina,
        'pode_adicionar_projeto': pode_adicionar_projeto,
        'pode_editar_projeto': pode_editar_projeto,
        'pode_apagar_projeto': pode_apagar_projeto
    })

def projeto_detail(request, projeto_id):
    projeto = Projeto.objects.get(pk=projeto_id)
    return render(request, 'curso/projeto_detail.html', {'projeto': projeto})

def curso_list(request):
    cursos = Curso.objects.all()

    # Inicializar permissões como `False` por padrão
    pode_adicionar = False
    pode_editar = False
    pode_apagar = False

    # Verificar permissões se o usuário estiver autenticado
    if request.user.is_authenticated:
        pode_adicionar = request.user.has_perm('curso.add_curso')
        pode_editar = request.user.has_perm('curso.change_curso')
        pode_apagar = request.user.has_perm('curso.delete_curso')

    contexto = {
        'cursos': cursos,
        'pode_adicionar': pode_adicionar,
        'pode_editar': pode_editar,
        'pode_apagar': pode_apagar
    }

    return render(request, 'curso/curso_list.html', contexto)
