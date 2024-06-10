from django.shortcuts import render

def home_view(request):
    return render(request, 'novaapp/home.html')

def about_view(request):
    return render(request, 'novaapp/about.html')

def contact_view(request):
    return render(request, 'novaapp/contact.html')

def games_view(request):
    return render(request, 'novaapp/games.html')
