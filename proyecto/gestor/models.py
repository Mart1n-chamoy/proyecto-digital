from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

# Create your models here.

TAMANO_MAXIMO_MB = 15

def validar_tamano_archivo(archivo):
   limite_bytes = TAMANO_MAXIMO_MB * 1024 * 1024
   if archivo.size > limite_bytes:
      raise ValidationError(f'El archivo no puede superar los {TAMANO_MAXIMO_MB} MB.')

class Documento(models.Model):
   id = models.AutoField(primary_key=True)
   nombre = models.CharField(max_length=100, verbose_name='Nombre')
   apellido = models.CharField(max_length=100, verbose_name='Apellido')
   dni = models.CharField(max_length=20, verbose_name='DNI')
   telefono = models.CharField(max_length=20, verbose_name='Teléfono', blank=True, default='')
   numero_contrato = models.CharField(max_length=50, verbose_name='Número de Contrato', blank=True, default='')
   parcela = models.CharField(max_length=100, verbose_name='Parcela')
   archivo = models.FileField(
      upload_to='documentos/',
      verbose_name='Archivo',
      validators=[FileExtensionValidator(['pdf']), validar_tamano_archivo],
   )
   creado_por = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
      related_name='documentos_creados', verbose_name='Creado por',
   )
   creado_en = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creado el')
   modificado_por = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
      related_name='documentos_modificados', verbose_name='Modificado por',
   )
   modificado_en = models.DateTimeField(auto_now=True, null=True, verbose_name='Modificado el')

   def __str__(self):
      fila = "Nombre: " + self.nombre +" - "+"Apellido: " + self.apellido +" - "+ "DNI: " + self.dni +" - "+ "Teléfono: " + self.telefono +" - "+ "Contrato: " + self.numero_contrato +" - "+ "Parcela: " + self.parcela
      return fila

   def delete(self, using=None, keep_parents=False):
      self.archivo.storage.delete(self.archivo.name)
      super().delete(using=using, keep_parents=keep_parents)


class RegistroAuditoria(models.Model):
   ACCION_CREAR = 'crear'
   ACCION_EDITAR = 'editar'
   ACCION_ELIMINAR = 'eliminar'
   ACCION_CHOICES = [
      (ACCION_CREAR, 'Creación'),
      (ACCION_EDITAR, 'Edición'),
      (ACCION_ELIMINAR, 'Eliminación'),
   ]

   usuario = models.ForeignKey(
      settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Usuario',
   )
   accion = models.CharField(max_length=10, choices=ACCION_CHOICES, verbose_name='Acción')
   documento_id = models.IntegerField(verbose_name='ID Documento')
   documento_descripcion = models.CharField(max_length=255, verbose_name='Documento')
   fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')

   class Meta:
      ordering = ['-fecha']
      verbose_name = 'Registro de auditoría'
      verbose_name_plural = 'Registros de auditoría'

   def __str__(self):
      return f'{self.get_accion_display()} - {self.documento_descripcion} ({self.fecha:%d/%m/%Y %H:%M})'