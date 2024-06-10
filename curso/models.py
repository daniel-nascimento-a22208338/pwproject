from django.db import models

class Razao(models.Model):
    razao = models.TextField()
    ordem = models.PositiveIntegerField()

    def __str__(self):
        return self.razao

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    razoes = models.ManyToManyField(Razao, related_name='cursos')
    coordenador = models.ForeignKey('Docente', related_name='coordenador_curso', on_delete=models.SET_NULL, null=True)
    secretario = models.ForeignKey('Docente', related_name='secretario_curso', on_delete=models.SET_NULL, null=True)
    diretor = models.ForeignKey('Docente', related_name='diretor_curso', on_delete=models.SET_NULL, null=True)
    competencias = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    cursos = models.ManyToManyField(Curso, related_name='disciplinas')
    carga_horaria = models.PositiveIntegerField()
    ano = models.PositiveIntegerField()
    semestre = models.CharField(max_length=20)
    ects = models.PositiveIntegerField()
    professores = models.ManyToManyField('Docente', related_name='disciplinas')

    def __str__(self):
        return self.nome

class Programacao(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Projeto(models.Model):
    nome = models.CharField(max_length=100)
    programacao = models.ForeignKey(Programacao, related_name='projetos', on_delete=models.CASCADE, null=True)
    disciplina = models.ForeignKey(Disciplina, related_name='projetos', on_delete=models.CASCADE)
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='imagens/', null=True, blank=True)
    video_demo = models.URLField(null=True, blank=True)
    github_repo = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Docente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    contato = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.nome
