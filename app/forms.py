from django import forms
from .models import Bairro, TipoResiduo, AgendaColeta

class BairroForm(forms.ModelForm):
    class Meta:
        model = Bairro
        fields = '__all__'

class AgendaForm(forms.ModelForm):
    class Meta:
        model = AgendaColeta
        fields = '__all__'