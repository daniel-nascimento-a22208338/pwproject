from django.contrib import admin
from .models import Pessoa, Leitor, Autor, Category, Article, Comment, Rating

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

class RatingInline(admin.StackedInline):
    model = Rating
    extra = 0

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'rating', 'views', 'get_comment_count', 'get_rating_count')
    list_filter = ('author', 'categories')
    search_fields = ('title', 'content')
    inlines = [CommentInline, RatingInline]

    def get_comment_count(self, obj):
        return obj.comments.count()
    get_comment_count.short_description = 'Comment Count'

    def get_rating_count(self, obj):
        return obj.ratings.count()
    get_rating_count.short_description = 'Rating Count'

class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'data_criacao')
    search_fields = ('nome', 'email')

class AutorAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'bio', 'redes_sociais', 'website', 'experiencia')
    search_fields = ('pessoa__nome', 'bio', 'redes_sociais', 'website', 'experiencia')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('pessoa')

    def get_articles(self, obj):
        return Article.objects.filter(author__pessoa=obj.pessoa)
    get_articles.short_description = 'Articles'

admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Leitor)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Rating)
