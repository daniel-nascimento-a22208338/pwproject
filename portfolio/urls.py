from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('logout/', views.logout_view, name="logout"),
    path('login/', views.login_view, name="login"),
    path('registro/', views.registro_view, name="registro"),
    path('', views.landing_page, name='landing_page'),
    path('mebyme/', views.mebyme, name='mebyme'),
    path('about/', views.about, name='about'),
]
