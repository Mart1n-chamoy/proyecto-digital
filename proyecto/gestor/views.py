from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def saludo(request):
    return HttpResponse("<h1>Bienvenido a la página del gestor.</h1>")
def inicio(request):
    return render(request, 'paginas/inicio.html')