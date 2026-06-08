from django.contrib import admin
from .models import (
    Bairro, 
    TipoResiduo, 
    AgendaColeta, 
    PontoColetaVoluntaria, 
    OcorrenciaZeladoria, 
    AlertaCidade, 
    EmpresaParceira,
    Manifestacao,          # 🗣️ Ouvidoria
    Imovel,                # 🧾 IPTU
    IPTU2026,              # 🧾 IPTU
    AgendamentoCataTreco,  # 🚛 NOVO: Cata-Treco
    RegistroColetaRealizada # 📋 NOVO: Histórico de Coletas
)

@admin.register(Bairro)
class BairroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'regiao', 'ativo')
    list_filter = ('regiao', 'ativo')
    search_fields = ('nome',)

@admin.register(TipoResiduo)
class TipoResiduoAdmin(admin.ModelAdmin):
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


# --- ✨ ADMIN DO MÓDULO DE OUVIDORIA MUNICIPAL ---
@admin.register(Manifestacao)
class ManifestacaoAdmin(admin.ModelAdmin):
    list_display = ('protocolo', 'tipo', 'assunto', 'status', 'data_criacao')
    list_filter = ('status', 'tipo', 'data_criacao')
    search_fields = ('protocolo', 'assunto', 'descricao')

    def get_readonly_fields(self, request, obj=None):
        """Bloqueia a alteração dos dados enviados pelo cidadão"""
        campos_base = ['protocolo', 'tipo', 'bairro', 'assunto', 'descricao', 'data_criacao']
        return [f for f in campos_base if hasattr(Manifestacao, f)]

    def get_fieldsets(self, request, obj=None):
        """Organiza os blocos visualmente baseado nos campos existentes no seu Model"""
        campo_resposta = 'resposta_admin' if hasattr(Manifestacao, 'resposta_admin') else 'resposta_ouvidoria'
        
        fields_cidadao = [f for f in ['protocolo', 'tipo', 'bairro', 'assunto', 'descricao', 'data_criacao'] if hasattr(Manifestacao, f)]
        
        return [
            ('Dados da Manifestação (Cidadão)', {
                'fields': fields_cidadao
            }),
            ('Despacho e Parecer Técnico (Prefeitura)', {
                'fields': ('status', campo_resposta)
            }),
        ]


# --- ADMIN DO MÓDULO DE IPTU E ARRECADAÇÃO CONTROLANDO ERROS DE CAMPOS ---
@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('inscricao_imobiliaria', 'proprietario', 'cpf_cnpj', 'bairro')
    list_filter = ('bairro',)
    search_fields = ('inscricao_imobiliaria', 'proprietario', 'cpf_cnpj')

@admin.register(IPTU2026)
class IPTU2026Admin(admin.ModelAdmin):
    list_display = [f.name for f in IPTU2026._meta.fields]
    search_fields = ('imovel__inscricao_imobiliaria', 'imovel__proprietario')


# --- 🚛 NOVO: ADMIN DO MÓDULO DE LOGÍSTICA E AGENDAMENTOS ESPECIAIS ---

@admin.register(AgendamentoCataTreco)
class AgendamentoCataTrecoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cidadao', 'bairro', 'data_solicitacao', 'data_agendada', 'status')
    list_filter = ('status', 'bairro')
    search_fields = ('endereco_completo', 'descricao_itens', 'cidadao__username')
    date_hierarchy = 'data_solicitacao'
    
    # Organiza a página de edição no admin por blocos de assunto
    fieldsets = [
        ('Informações do Solicitante', {
            'fields': ('cidadao', 'bairro', 'endereco_completo')
        }),
        ('Detalhes do Descarte', {
            'fields': ('descricao_itens', 'data_solicitacao')
        }),
        ('Gerenciamento da Prefeitura', {
            'fields': ('status', 'data_agendada', 'observacoes_prefeitura')
        }),
    ]
    readonly_fields = ('data_solicitacao',)


@admin.register(RegistroColetaRealizada)
class RegistroColetaRealizadaAdmin(admin.ModelAdmin):
    list_display = ('agenda', 'data_execucao', 'horario_registro', 'motorista_ou_equipe')
    list_filter = ('data_execucao', 'agenda__bairro')
    search_fields = ('motorista_ou_equipe', 'ocorrencia_na_rota', 'agenda__bairro__nome')
    date_hierarchy = 'data_execucao'