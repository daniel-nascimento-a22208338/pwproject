from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    interesses = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Leitor(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Autor(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE)
    bio = models.TextField()
    redes_sociais = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    experiencia = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.pessoa.nome

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey (Autor, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(Leitor, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.commenter.username} on {self.article.title}'

class Rating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    rater = models.ForeignKey(Leitor, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(choices=((1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.article.title} rated {self.value} stars by {self.rater.username}'
