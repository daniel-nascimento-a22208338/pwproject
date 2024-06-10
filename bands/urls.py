from django.urls import path
from . import views

app_name = 'bands'

urlpatterns = [
    path('criar/musica/<int:album_id>/', views.criar_musica_view, name='criar_musica'),
    path('editar/musica/<int:musica_id>/', views.editar_musica_view, name='editar_musica'),
    path('apagar/musica/<int:musica_id>/', views.apagar_musica_view, name='apagar_musica'),
    path('criar/album/', views.criar_album_view, name='criar_album'),
    path('editar/album/<int:album_id>/', views.editar_album_view, name='editar_album'),
    path('apagar/album/<int:album_id>/', views.apagar_album_view, name='apagar_album'),
    path('criar-banda/', views.criar_banda_view, name='criar_banda'),
    path('editar-banda/<int:banda_id>/', views.editar_banda_view, name='editar_banda'),
    path('apagar-banda/<int:banda_id>/', views.apagar_banda_view, name='apagar_banda'),
    path('', views.bandas_list_view, name='bandas_list'),
    path('registro/', views.registo_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('banda/<int:banda_id>/', views.detalhes_banda_view, name='detalhes_banda'),
    path('album/<int:album_id>/', views.detalhes_album_view, name='detalhes_album'),
    path('musica/<int:musica_id>/', views.detalhes_musica_view, name='detalhes_musica'),

]
