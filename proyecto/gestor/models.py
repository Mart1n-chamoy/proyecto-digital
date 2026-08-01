from django.db import models

# Create your models here.

class Documento(models.Model):
   id = models.AutoField(primary_key=True)
   nombre = models.CharField(max_length=100, verbose_name='Nombre')
   apellido = models.CharField(max_length=100, verbose_name='Apellido')
   dni = models.CharField(max_length=20, verbose_name='DNI')
   parcela = models.CharField(max_length=100, verbose_name='Parcela')
   archivo = models.FileField(upload_to='documentos/', verbose_name='Archivo')


def __str__(self):
    fila = "Nombre: " + self.nombre + " - Apellido: " + self.apellido + " - DNI: " + self.dni + " - Parcela: " + self.parcela
    return fila

def delete(self, using=None, keep_parents=False):
    # Eliminar el archivo asociado al documento
    self.archivo.storage.delete(self.archivo.name)
    # Llamar al método delete() de la clase padre para eliminar el registro de la base de datos
    super().delete()