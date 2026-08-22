from django.contrib import admin
from .models import Documento, RegistroAuditoria
# Register your models here.

admin.site.register(Documento)


@admin.register(RegistroAuditoria)
class RegistroAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'documento_id', 'documento_descripcion')
    list_filter = ('accion',)
    readonly_fields = [f.name for f in RegistroAuditoria._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
