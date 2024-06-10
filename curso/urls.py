# No arquivo urls.py

from django.urls import path
from . import views
from .views import CustomLoginView

app_name='curso'

urlpatterns = [
    path('disciplina/<int:disciplina_id>/projetos/criar/', views.criar_projeto_view, name='criar_projeto'),
    path('projetos/editar/<int:projeto_id>/', views.editar_projeto_view, name='editar_projeto'),
    path('projetos/apagar/<int:projeto_id>/', views.apagar_projeto_view, name='apagar_projeto'),
    path('curso/<int:curso_id>/disciplinas/criar/', views.criar_disciplina_view, name='criar_disciplina'),
    path('disciplinas/editar/<int:disciplina_id>/', views.editar_disciplina_view, name='editar_disciplina'),
    path('disciplinas/apagar/<int:disciplina_id>/', views.apagar_disciplina_view, name='apagar_disciplina'),
    path('criar/', views.criar_curso_view, name='criar_curso'),
    path('editar/<int:curso_id>/', views.editar_curso_view, name='editar_curso'),
    path('apagar/<int:curso_id>/', views.apagar_curso_view, name='apagar_curso'),
    path('', views.curso_list, name='cursos'),  # Página padrão de cursos
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.CursoLogoutView.as_view(), name='logout'),
    path('register/', views.registro_view, name='register'),
    path('curso/<int:curso_id>/', views.curso_detail, name='curso_detail'),
    path('disciplina/<int:disciplina_id>/', views.disciplina_detail, name='disciplina_detail'),
    path('projeto/<int:projeto_id>/', views.projeto_detail, name='projeto_detail'),
]
