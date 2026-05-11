from django.contrib import admin
from .models import Bairro, TipoResiduo, AgendaColeta

@admin.register(Bairro)
class BairroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_cadastro', 'ativo')
    search_fields = ('nome',)

@admin.register(TipoResiduo)
class TipoResiduoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cor_hex', 'ativo')

@admin.register(AgendaColeta)
class AgendaColetaAdmin(admin.ModelAdmin):
    list_display = ('bairro', 'dia_semana', 'horario', 'tipo', 'ativo')
    list_filter = ('dia_semana', 'bairro', 'tipo')