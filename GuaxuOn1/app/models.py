from django.db import models
from django.contrib.auth.models import User
import uuid

# --- MODELOS BASE ---

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


# --- MÓDULO INTEGRADO DE OUVIDORIA MUNICIPAL ---

class Manifestacao(models.Model):
    TIPO_CHOICES = [
        ('RECLAMACAO', 'Reclamação'),
        ('DENUNCIA', 'Denúncia'),
        ('SUGESTAO', 'Sugestão'),
        ('ELOGIO', 'Elogio'),
    ]
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente de Análise'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('RESOLVIDO', 'Resolvido'),
    ]

    # Gera um protocolo único automaticamente (Ex: 4A2B7C8D)
    protocolo = models.CharField(max_length=8, unique=True, editable=False)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='RECLAMACAO')
    assunto = models.CharField(max_length=100)
    descricao = models.TextField(verbose_name="Descrição do Fato")
    
    # ✨ Vincula o ticket ao usuário criador
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cidadão Autor")

    # Integrado diretamente com a sua tabela de Bairros oficial
    bairro = models.ForeignKey(Bairro, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Bairro Ocorrido")
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDENTE')
    resposta_admin = models.TextField(blank=True, null=True, verbose_name="Resposta da Ouvidoria")

    def save(self, *args, **kwargs):
        if not self.protocolo:
            self.protocolo = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_display()} - Prot: {self.protocolo}"


# --- MÓDULO INTEGRADO DE ARRECADAÇÃO E IPTU 2026 ---

class Imovel(models.Model):
    """Representa um imóvel cadastrado no município de Guaxupé e região"""
    inscricao_imobiliaria = models.CharField(max_length=20, unique=True, verbose_name="Inscrição Imobiliária (Código)")
    proprietario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Proprietário Cadastrado")
    cpf_cnpj = models.CharField(max_length=18, verbose_name="CPF/CNPJ do Titular")
    endereco = models.CharField(max_length=255, verbose_name="Endereço do Imóvel")
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT, verbose_name="Bairro")
    valor_venal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Venal (R$)")

    def __str__(self):
        return f"Insc: {self.inscricao_imobiliaria} - {self.endereco}"


class IPTU2026(models.Model):
    """Guias de pagamento e parcelas do IPTU de cada imóvel"""
    FORMA_PAGAMENTO = [
        ('COTA_UNICA', 'Cota Única (Com Desconto)'),
        ('PARCELA', 'Parcela Mensal'),
    ]
    
    STATUS_PAGAMENTO = [
        ('ABERTO', 'Aberto / Aguardando'),
        ('PAGO', 'Pago / Compensado'),
        ('VENCIDO', 'Vencido'),
    ]

    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name='debitos')
    exercicio = models.IntegerField(default=2026)
    parcela_numero = models.IntegerField(help_text="0 para Cota Única, 1 a 10 para parcelas normais")
    tipo_cobranca = models.CharField(max_length=15, choices=FORMA_PAGAMENTO, default='PARCELA')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_PAGAMENTO, default='ABERTO')
    linha_digitavel = models.CharField(max_length=50, blank=True, null=True, verbose_name="Linha Digitável do Boleto")
    codigo_pix = models.TextField(blank=True, null=True, verbose_name="Copia e Cola PIX da Prefeitura")

    def __str__(self):
        return f"{self.imovel.inscricao_imobiliaria} - 2026/{self.parcela_numero} ({self.status})"


# --- MÓDULO DE AGENDAMENTOS ESPECIAIS E LOGÍSTICA ---

class AgendamentoCataTreco(models.Model):
    """Solicitação de recolhimento de grandes volumes (sofás, podas, eletrodomésticos)"""
    STATUS_AGENDAMENTO = [
        ('AGUARDANDO', 'Aguardando Aprovação'),
        ('AGENDADO', 'Coleta Agendada'),
        ('RECOLHIDO', 'Material Recolhido'),
        ('CANCELADO', 'Cancelado'),
    ]

    cidadao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Cidadão Solicitante")
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT, verbose_name="Bairro de Retirada")
    endereco_completo = models.CharField(max_length=255, verbose_name="Endereço de Recolhimento")
    descricao_itens = models.TextField(help_text="Ex: 1 sofá velho e 1 geladeira quebrada")
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    data_agendada = models.DateField(null=True, blank=True, verbose_name="Data Marcada para Recolhimento")
    status = models.CharField(max_length=15, choices=STATUS_AGENDAMENTO, default='AGUARDANDO')
    observacoes_prefeitura = models.TextField(blank=True, null=True, verbose_name="Notas da Zeladoria")

    class Meta:
        verbose_name = "Agendamento Cata-Treco"
        verbose_name_plural = "Agendamentos Cata-Treco"

    def __str__(self):
        return f"Cata-Treco #{self.id} - {self.bairro.nome} ({self.status})"


class RegistroColetaRealizada(models.Model):
    """Histórico de passagens dos caminhões para controle interno e auditoria"""
    agenda = models.ForeignKey(AgendaColeta, on_delete=models.CASCADE, verbose_name="Rota da Agenda")
    data_execucao = models.DateField(verbose_name="Data da Coleta")
    horario_registro = models.DateTimeField(auto_now_add=True, verbose_name="Hora do Registro")
    motorista_ou_equipe = models.CharField(max_length=100, blank=True, null=True, verbose_name="Equipe/Caminhão")
    ocorrencia_na_rota = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        help_text="Ex: Rota concluída com atraso devido à chuva / Carro obstruindo via"
    )

    class Meta:
        verbose_name = "Registro de Coleta Realizada"
        verbose_name_plural = "Registros de Coletas Realizadas"
        ordering = ['-horario_registro']

    def __str__(self):
        return f"Coleta efetuada em {self.data_execucao} - {self.agenda.bairro.nome}"