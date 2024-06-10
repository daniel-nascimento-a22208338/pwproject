from django.shortcuts import render
from datetime import date

def index_view(request):
    return render(request, 'pwsite/index.html',{
        'data': date.today()
 })

def about_view(request):
    return render(request, 'pwsite/sobre.html',{
         'data': date.today()
        })

def interests_view(request):
    return render(request, 'pwsite/interesses.html',{
         'data': date.today()
        })
