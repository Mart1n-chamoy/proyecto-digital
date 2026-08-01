from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def inicio(request):
    return render(request, 'paginas/inicio.html')
def documentos(request):
    return render(request, 'documentos/index.html')
def crear_documento(request):
    return render(request, 'documentos/crear.html')
def editar_documento(request):
    return render(request, 'documentos/editar.html')
