from django.urls import path
from . import views

app_name='meteo'

urlpatterns = [
    path('', views.previsao_lisboa, name='previsao_lisboa'),
    path('lisboa/', views.previsao_lisboa, name='previsao_lisboa'),
    path('previsao/', views.previsao_cidade, name='previsao_cidade'),
    path('descricao-apis/', views.descricao_apis, name='descricao_apis'),
]
