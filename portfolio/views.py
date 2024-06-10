from django.shortcuts import render, redirect
import requests
from django.contrib.auth import models, authenticate, login, logout

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('portfolio:landing_page')

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return render(request, 'portfolio/landing_page.html')
        else:
            render(request, 'portfolio/login.html', {
                'mensagem':'Credenciais invalidas'
            })
    return render(request, 'portfolio/login.html')

def registro_view(request):
    if request.method == "POST":
        models.User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            first_name=request.POST['nome'],
            last_name=request.POST['apelido'],
            password=request.POST['password']
        )
        return redirect('portfolio:login')

    return render(request, 'portfolio/registro.html' )


def get_weather_icon_for_lisboa():
    cidade_id = 1110600  # ID de Lisboa na API do IPMA
    previsao_url = f'https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{cidade_id}.json'
    classes_tempo_url = 'https://api.ipma.pt/open-data/weather-type-classe.json'

    previsao_res = requests.get(previsao_url)
    classes_res = requests.get(classes_tempo_url)

    if previsao_res.status_code == 200 and classes_res.status_code == 200:
        previsao_data = previsao_res.json()
        classes_data = classes_res.json()

        hoje_previsao = previsao_data['data'][0]
        id_weather_type = hoje_previsao['idWeatherType']

        if isinstance(classes_data, dict) and 'data' in classes_data:
            classes_data = classes_data['data']

        icon_name = f'w_ic_d_{id_weather_type:02}anim.svg'
        icon_url = f'/static/meteo/icons/{icon_name}'

        return icon_url
    else:
        return None

def landing_page(request):
    weather_icon_url = get_weather_icon_for_lisboa()

    return render(request, 'portfolio/landing_page.html', {
        'weather_icon_url': weather_icon_url
    })

def mebyme(request):
    return render(request, 'portfolio/mebyme.html')

def about(request):
    return render(request, 'portfolio/about.html')
