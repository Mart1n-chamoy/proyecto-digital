from django import forms
from .models import Documento

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        exclude = ['creado_por', 'creado_en', 'modificado_por', 'modificado_en']
