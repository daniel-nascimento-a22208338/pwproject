from django.shortcuts import render, get_object_or_404
from .models import Regiao, Praia

def lista_praias(request):
    regioes = Regiao.objects.all()
    return render(request, 'praias/lista_praias.html', {'regioes': regioes})

def detalhes_praia(request, praia_id):
    praia = get_object_or_404(Praia, pk=praia_id)
    return render(request, 'praias/detalhes_praia.html', {'praia': praia})
