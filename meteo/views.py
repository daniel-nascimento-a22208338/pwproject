import requests
from django.shortcuts import render
from django.http import JsonResponse

def get_cidades():
    url = "https://api.ipma.pt/open-data/distrits-islands.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        cidades = {}

        for cidade in data.get('data', []):
            cidades[cidade['globalIdLocal']] = cidade['local']

        return cidades
    else:
        return {}

def adicionar_cidades_ao_contexto(contexto):
    cidades = get_cidades()
    contexto['cidades'] = cidades
    return contexto

def previsao_lisboa(request):
    cidade_id = 1110600  # ID de Lisboa na API do IPMA
    cidades = get_cidades()
    nome_cidade = cidades.get(cidade_id, 'Lisboa')
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

        descricao_tempo = next(
            (item.get('descIdWeatherTypePT', 'Descrição não disponível') for item in classes_data if item['idWeatherType'] == id_weather_type),
            'Descrição não disponível'
        )
        icon_name = f'w_ic_d_{id_weather_type:02}anim.svg'
        icon_url = f'/static/meteo/icons/{icon_name}'

        contexto = {
            'cidade': nome_cidade,
            'temp_min': hoje_previsao['tMin'],
            'temp_max': hoje_previsao['tMax'],
            'data': hoje_previsao['forecastDate'],
            'descricao_tempo': descricao_tempo,
            'icon_url': icon_url,
            'cidade_id': cidade_id,
        }
        contexto = adicionar_cidades_ao_contexto(contexto)
        return render(request, 'meteo/previsao_lisboa.html', contexto)
    else:
        return render(request, 'meteo/erro.html')

def previsao_cidade(request):
    cidades = get_cidades()

    if 'cidade' in request.GET:
        cidade_id = request.GET['cidade']
        nome_cidade = cidades.get(int(cidade_id), 'Cidade Desconhecida')
        previsao_url = f'https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{cidade_id}.json'
        classes_tempo_url = 'https://api.ipma.pt/open-data/weather-type-classe.json'
        previsao_res = requests.get(previsao_url)
        classes_res = requests.get(classes_tempo_url)

        if previsao_res.status_code == 200 and classes_res.status_code == 200:
            previsao_data = previsao_res.json()
            classes_data = classes_res.json()

            if isinstance(classes_data, dict) and 'data' in classes_data:
                classes_data = classes_data['data']

            previsoes = []
            for item in previsao_data['data'][:5]:
                id_weather_type = item['idWeatherType']
                descricao_tempo = next(
                    (c_item.get('descIdWeatherTypePT', 'Descrição não disponível') for c_item in classes_data if c_item['idWeatherType'] == id_weather_type),
                    'Descrição não disponível'
                )
                icon_name = f'w_ic_d_{id_weather_type:02}anim.svg'
                icon_url = f'/static/meteo/icons/{icon_name}'
                previsoes.append({
                    'data': item['forecastDate'],
                    'temp_min': item['tMin'],
                    'temp_max': item['tMax'],
                    'descricao_tempo': descricao_tempo,
                    'icon_url': icon_url
                })

            contexto = {
                'cidade': nome_cidade,
                'cidade_id': cidade_id,
                'previsoes': previsoes,
            }
            contexto = adicionar_cidades_ao_contexto(contexto)
            return render(request, 'meteo/previsao_cidade.html', contexto)

    contexto = {
        'cidade': None,
        'cidade_id': None,
        'previsoes': None,
    }
    contexto = adicionar_cidades_ao_contexto(contexto)
    return render(request, 'meteo/previsao_cidade.html', contexto)

def descricao_apis(request):
    # URLs das APIs
    weather_types_url = "https://api.ipma.pt/open-data/weather-type-classe.json"
    distrits_islands_url = "https://api.ipma.pt/open-data/distrits-islands.json"

    # Requisições GET para as APIs
    weather_types_response = requests.get(weather_types_url)
    distrits_islands_response = requests.get(distrits_islands_url)

    # Verifica se as requisições foram bem-sucedidas
    if weather_types_response.status_code == 200:
        weather_types_data = weather_types_response.json()
    else:
        weather_types_data = {"data": "Erro ao obter os dados de tipos de clima."}

    if distrits_islands_response.status_code == 200:
        distrits_islands_data = distrits_islands_response.json()
    else:
        distrits_islands_data = {"data": "Erro ao obter os dados de distritos e ilhas."}

    # Renderiza o template com os dados das APIs
    return render(request, 'meteo/descricao_apis.html', {
        'weather_types': weather_types_data,
        'distrits_islands': distrits_islands_data,
        'weather_types_url': weather_types_url,
        'distrits_islands_url': distrits_islands_url
    })
