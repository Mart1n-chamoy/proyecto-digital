from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from .models import Documento, RegistroAuditoria
from .forms import DocumentoForm
# Create your views here.

DOCUMENTOS_POR_PAGINA = 20

@login_required
def inicio(request):
    total_documentos = Documento.objects.count()
    return render(request, 'paginas/inicio.html', {'total_documentos': total_documentos})
@login_required
def documentos(request):
    query = request.GET.get('q', '')
    documentos = Documento.objects.all().order_by('-id')
    if query:
        documentos = documentos.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(dni__icontains=query) |
            Q(numero_contrato__icontains=query) |
            Q(parcela__icontains=query)
        )
    paginator = Paginator(documentos, DOCUMENTOS_POR_PAGINA)
    pagina = paginator.get_page(request.GET.get('page'))
    return render(request, 'documentos/index.html', {'documentos': pagina, 'query': query})
@permission_required('gestor.add_documento', raise_exception=True)
def crear_documento(request):
    formulario = DocumentoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        documento = formulario.save(commit=False)
        documento.creado_por = request.user
        documento.save()
        RegistroAuditoria.objects.create(
            usuario=request.user,
            accion=RegistroAuditoria.ACCION_CREAR,
            documento_id=documento.id,
            documento_descripcion=str(documento),
        )
        return redirect('documentos')
    return render(request, 'documentos/crear.html', {'formulario': formulario})
@permission_required('gestor.change_documento', raise_exception=True)
def editar_documento(request, id):
    documento = Documento.objects.get(id=id)
    formulario = DocumentoForm(request.POST or None, request.FILES or None, instance=documento)
    if formulario.is_valid() and request.method == 'POST':
        documento = formulario.save(commit=False)
        documento.modificado_por = request.user
        documento.save()
        RegistroAuditoria.objects.create(
            usuario=request.user,
            accion=RegistroAuditoria.ACCION_EDITAR,
            documento_id=documento.id,
            documento_descripcion=str(documento),
        )
        return redirect('documentos')
    return render(request, 'documentos/editar.html', {'formulario': formulario})

@permission_required('gestor.delete_documento', raise_exception=True)
def eliminar_documento(request, id):
    documento = Documento.objects.get(id=id)
    if request.method == 'POST':
        RegistroAuditoria.objects.create(
            usuario=request.user,
            accion=RegistroAuditoria.ACCION_ELIMINAR,
            documento_id=documento.id,
            documento_descripcion=str(documento),
        )
        documento.delete()
        return redirect('documentos')
    return render(request, 'documentos/eliminar.html', {'documento': documento})

@permission_required('gestor.view_registroauditoria', raise_exception=True)
def auditoria(request):
    registros = RegistroAuditoria.objects.select_related('usuario').all()
    paginator = Paginator(registros, DOCUMENTOS_POR_PAGINA)
    pagina = paginator.get_page(request.GET.get('page'))
    return render(request, 'documentos/auditoria.html', {'registros': pagina})