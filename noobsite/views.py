from django.http import HttpResponse

def index_view(request):
    return HttpResponse("Olá n00b, esta é a página web mais básica do mundo!")

def about_view(request):
    return HttpResponse("Esta é a página 'Sobre Nós' do site.")

def contact_view(request):
    return HttpResponse("Página de contato - Envie-nos um e-mail para contato.")

def products_view(request):
    return HttpResponse("Nossos produtos estão em breve! Volte em breve para mais informações.")
