from django.contrib import admin
from .models import (
    Bairro, 
    TipoResiduo, 
    AgendaColeta, 
    PontoColetaVoluntaria, 
    OcorrenciaZeladoria, 
    AlertaCidade, 
    EmpresaParceira
)

@admin.register(Bairro)
class BairroAdmin(admin.ModelAdmin):
    # Removido 'data_cadastro' que não existia no modelo Bairro
    list_display = ('nome', 'regiao', 'ativo')
    list_filter = ('regiao', 'ativo')
    search_fields = ('nome',)

@admin.register(TipoResiduo)
class TipoResiduoAdmin(admin.ModelAdmin):
    # Corrigido de 'cor_hex' para 'cor_identificacao' e removido 'ativo'
    list_display = ('nome', 'cor_identificacao', 'descricao')
    search_fields = ('nome',)

@admin.register(AgendaColeta)
class AgendaColetaAdmin(admin.ModelAdmin):
    list_display = ('bairro', 'tipo', 'dia_semana', 'horario', 'ativo')
    list_filter = ('dia_semana', 'ativo', 'tipo')
    search_fields = ('bairro__nome',)

@admin.register(PontoColetaVoluntaria)
class PontoColetaVoluntariaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'bairro', 'ativo')
    list_filter = ('bairro', 'ativo')
    search_fields = ('nome', 'endereco')

@admin.register(OcorrenciaZeladoria)
class OcorrenciaZeladoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cidadao', 'bairro', 'status', 'data_abertura')
    list_filter = ('status', 'bairro')
    search_fields = ('descricao_problema', 'cidadao__username')

@admin.register(AlertaCidade)
class AlertaCidadeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'nivel', 'data_publicacao', 'data_expiracao', 'ativo')
    list_filter = ('nivel', 'ativo')
    search_fields = ('titulo', 'mensagem')

@admin.register(EmpresaParceira)
class EmpresaParceiraAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'telefone', 'responsavel')
    search_fields = ('nome_fantasia', 'responsavel')