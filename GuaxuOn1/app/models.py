from django.db import models
from django.contrib.auth.models import User

# --- MODELOS BASE (MANTIDOS E CORRIGIDOS) ---

class Bairro(models.Model):
    nome = models.CharField(max_length=100)
    # null=True e blank=True evitam o travamento ao rodar as migrações
    regiao = models.CharField(max_length=100, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class TipoResiduo(models.Model):
    nome = models.CharField(max_length=50)  # Ex: Orgânico, Reciclável, Eletrônico
    
    # Adicionamos default, null e blank para o Django NUNCA mais travar aqui
    cor_identificacao = models.CharField(max_length=7, default='#888888', null=True, blank=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class AgendaColeta(models.Model):
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoResiduo, on_delete=models.CASCADE)
    
    # === NOVO CAMPO ADICIONADO COM SEGURANÇA ===
    rua = models.CharField(max_length=255, default="Geral / Todas as Ruas", blank=True, null=True)
    
    dia_semana = models.CharField(max_length=20)  # Ex: Segunda-feira
    horario = models.TimeField()
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bairro.nome} - {self.rua} - {self.tipo.nome} ({self.dia_semana})"


# --- NOVOS MODELOS PARA EXPANDIR O BANCO DE DADOS (ZELADORIA E SINALIZAÇÃO) ---

class PontoColetaVoluntaria(models.Model):
    """Locais fixos na cidade para descarte de materiais específicos (PEVs)"""
    nome = models.CharField(max_length=100)  # Ex: EcoPonto Jardim Amaryllis
    endereco = models.CharField(max_length=255)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT)
    types_aceitos = models.ManyToManyField(TipoResiduo)
    ponto_referencia = models.CharField(max_length=150, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class OcorrenciaZeladoria(models.Model):
    """Problemas relatados pelos cidadãos (Lixo acumulado, descarte irregular, falta de capina)"""
    STATUS_CHOICES = [
        ('Aberto', 'Aberto/Pendente'),
        ('Analise', 'Em Análise pela Prefeitura'),
        ('Resolvido', 'Resolvido/Concluído'),
    ]
    
    cidadao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Cidadão")
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    descricao_problema = models.TextField()
    foto = models.ImageField(upload_to='ocorrencias/', blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Aberto')
    data_abertura = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ocorrência #{self.id} - {self.bairro.nome} ({self.status})"


class AlertaCidade(models.Model):
    """Avisos urgentes (Ex: Caminhão quebrado, alteração de rota devido a feriado)"""
    NIVEL_URGENCIA = [
        ('Informativo', 'Informativo (Azul)'),
        ('Atencao', 'Atenção (Amarelo)'),
        ('Critico', 'Crítico (Vermelho)'),
    ]

    titulo = models.CharField(max_length=150)
    mensagem = models.TextField()
    nivel = models.CharField(max_length=15, choices=NIVEL_URGENCIA, default='Informativo')
    data_publicacao = models.DateTimeField(auto_now_add=True)
    data_expiracao = models.DateTimeField(help_text="Data até quando o alerta deve aparecer na tela")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class EmpresaParceira(models.Model):
    """Cooperativas e empresas de reciclagem ligadas ao GuaxuON"""
    nome_fantasia = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    responsavel = models.CharField(max_length=100, blank=True, null=True)
    site_ou_rede_social = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nome_fantasia