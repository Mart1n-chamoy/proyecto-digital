from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Documento
from .forms import DocumentoForm
# Create your views here.

def inicio(request):
    return render(request, 'paginas/inicio.html')
def documentos(request):
    documentos = Documento.objects.all()
    return render(request, 'documentos/index.html', {'documentos': documentos})
def crear_documento(request):
    formulario = DocumentoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('documentos')
    return render(request, 'documentos/crear.html', {'formulario': formulario})
def editar_documento(request, id):
    documento = Documento.objects.get(id=id)
    formulario = DocumentoForm(request.POST or None, request.FILES or None, instance=documento)
    if formulario.is_valid() and request.method == 'POST':
        formulario.save()
        return redirect('documentos')
    return render(request, 'documentos/editar.html', {'formulario': formulario})

def eliminar_documento(request, id):
    documento = Documento.objects.get(id=id)
    documento.delete()
    return redirect('documentos')