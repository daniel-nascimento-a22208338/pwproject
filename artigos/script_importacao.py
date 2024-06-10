import json
from artigos.models import Pessoa, Leitor, Autor, Category, Article, Comment, Rating

# Load the JSON data
with open('artigos/initial_data.json', 'r') as file:
    data = json.load(file)

# Import Pessoa data
for pessoa_data in data['Pessoa']:
    pessoa, created = Pessoa.objects.get_or_create(
        id=pessoa_data['id'],
        defaults={
            'nome': pessoa_data['nome'],
            'email': pessoa_data['email'],
            'data_criacao': pessoa_data['data_criacao'],
            'foto_perfil': pessoa_data.get('foto_perfil', ''),
            'interesses': pessoa_data.get('interesses', '')
        }
    )

# Import Leitor data
for leitor_data in data['Leitor']:
    pessoa, created = Pessoa.objects.get_or_create(id=leitor_data['pessoa_id'])
    Leitor.objects.get_or_create(
        id=leitor_data['id'],
        defaults={
            'pessoa': pessoa,
            'username': leitor_data['username'],
            'email': leitor_data['email'],
            'date_joined': leitor_data['date_joined']
        }
    )

# Import Autor data
for autor_data in data['Autor']:
    pessoa, created = Pessoa.objects.get_or_create(id=autor_data['pessoa_id'])
    Autor.objects.get_or_create(
        id=autor_data['id'],
        defaults={
            'pessoa': pessoa,
            'bio': autor_data['bio'],
            'redes_sociais': autor_data.get('redes_sociais', ''),
            'website': autor_data.get('website', ''),
            'experiencia': autor_data.get('experiencia', '')
        }
    )

# Import Category data
for category_data in data['Category']:
    Category.objects.get_or_create(
        id=category_data['id'],
        defaults={'name': category_data['name']}
    )

# Import Article data
for article_data in data['Article']:
    author, created = Autor.objects.get_or_create(id=article_data['author_id'])
    article, created = Article.objects.get_or_create(
        id=article_data['id'],
        defaults={
            'title': article_data['title'],
            'content': article_data['content'],
            'author': author,
            'created_at': article_data['created_at'],
            'updated_at': article_data['updated_at'],
            'rating': article_data['rating'],
            'views': article_data['views']
        }
    )
    if created:
        article.categories.set(Category.objects.filter(id__in=article_data.get('categories', [])))

# Import Comment data
for comment_data in data['Comment']:
    article, created = Article.objects.get_or_create(id=comment_data['article_id'])
    commenter, created = Leitor.objects.get_or_create(id=comment_data['commenter_id'])
    Comment.objects.get_or_create(
        id=comment_data['id'],
        defaults={
            'article': article,
            'commenter': commenter,
            'content': comment_data['content'],
            'created_at': comment_data['created_at']
        }
    )

# Import Rating data
for rating_data in data['Rating']:
    article, created = Article.objects.get_or_create(id=rating_data['article_id'])
    rater, created = Leitor.objects.get_or_create(id=rating_data['rater_id'])
    Rating.objects.get_or_create(
        id=rating_data['id'],
        defaults={
            'article': article,
            'rater': rater,
            'value': rating_data['value'],
            'created_at': rating_data['created_at']
        }
    )

print("Dados importados com sucesso!")
