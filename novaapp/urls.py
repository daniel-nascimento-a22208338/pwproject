from django.urls import path
from . import views

app_name = 'novaapp'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('games/',views.games_view, name='games'),
]
