from django.urls import path
from . import views

app_name = 'praias'

urlpatterns = [
    path('', views.lista_praias, name='lista_praias'),
    path('praia/<int:praia_id>/', views.detalhes_praia, name='detalhes_praia'),
]
