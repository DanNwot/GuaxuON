from django.db import models

class BaseModel(models.Model):
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    ativo = models.BooleanField(default=True, verbose_name="Registro Ativo")

    class Meta:
        abstract = True

class Bairro(BaseModel):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Bairro")
    
    def __str__(self):
        return self.nome

class TipoResiduo(BaseModel):
    nome = models.CharField(max_length=100, verbose_name="Tipo de Resíduo")
    cor_hex = models.CharField(max_length=7, default="#343a40", verbose_name="Cor")

    def __str__(self):
        return self.nome

class AgendaColeta(BaseModel):
    DIAS = [('SEG', 'Segunda'), ('TER', 'Terça'), ('QUA', 'Quarta'), ('QUI', 'Quinta'), ('SEX', 'Sexta'), ('SAB', 'Sábado')]
    
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE, related_name="agendas")
    tipo = models.ForeignKey(TipoResiduo, on_delete=models.PROTECT)
    dia_semana = models.CharField(max_length=3, choices=DIAS)
    horario = models.TimeField()

    class Meta:
        verbose_name = "Agenda de Coleta"