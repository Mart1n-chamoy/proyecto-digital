from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Documento
from .forms import DocumentoForm
# Create your views here.

def inicio(request):
    return render(request, 'paginas/inicio.html')
def documentos(request):
    query = request.GET.get('q', '')
    documentos = Documento.objects.all()
    if query:
        documentos = documentos.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(dni__icontains=query) |
            Q(parcela__icontains=query)
        )
    return render(request, 'documentos/index.html', {'documentos': documentos, 'query': query})
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