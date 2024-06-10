from django.urls import path
from . import views
from .views import CustomLoginView

app_name = 'artigos'

urlpatterns= [
    path('artigos/<int:artigo_id>/comentarios/criar/', views.criar_comentario_view, name='criar_comentario'),
    path('comentarios/editar/<int:comentario_id>/', views.editar_comentario_view, name='editar_comentario'),
    path('comentarios/apagar/<int:comentario_id>/', views.apagar_comentario_view, name='apagar_comentario'),
    path('criar/', views.criar_artigo_view, name='criar_artigo'),
    path('editar/<int:artigo_id>/', views.editar_artigo_view, name='editar_artigo'),
    path('apagar/<int:artigo_id>/', views.apagar_artigo_view, name='apagar_artigo'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.registro_view, name='register'),
    path('', views.artigos_list_view, name='artigos_list'),
    path('artigo/<int:artigo_id>/', views.detalhes_artigo_view, name='detalhes_artigo'),
    path('autor/<int:autor_id>/', views.detalhes_autor_view, name='detalhes_autor'),
    path('leitor/<int:leitor_id>/', views.detalhes_leitor_view, name='detalhes_leitor'),
]