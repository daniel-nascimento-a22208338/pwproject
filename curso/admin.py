from django.contrib import admin
from .models import Razao, Curso, Disciplina, Programacao, Projeto, Docente

# Registrar o modelo Razao no admin
@admin.register(Razao)
class RazaoAdmin(admin.ModelAdmin):
    list_display = ('razao', 'ordem')

# Registrar o modelo Curso no admin
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'coordenador', 'secretario', 'diretor')
    list_filter = ('coordenador', 'secretario', 'diretor')

# Registrar o modelo Disciplina no admin
@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'carga_horaria', 'ano', 'semestre', 'ects')
    filter_horizontal = ('cursos', 'professores')

# Registrar o modelo Programacao no admin
@admin.register(Programacao)
class ProgramacaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)

# Registrar o modelo Projeto no admin
@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'disciplina', 'programacao', 'descricao')
    list_filter = ('disciplina', 'programacao')

# Registrar o modelo Docente no admin
@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'contato')

