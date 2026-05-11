from django.shortcuts import render
from .models import AgendaColeta, Bairro # Verifique se Bairro está importado
from datetime import datetime

def index(request):
    dias = [
        'Segunda-feira', 'Terça-feira', 'Quarta-feira', 
        'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'
    ]
    hoje_num = datetime.now().weekday()
    dia_atual = dias[hoje_num]

    coletas_hoje = AgendaColeta.objects.filter(dia_semana=dia_atual, ativo=True)

    context = {
        'dia_atual': dia_atual,
        'coletas_hoje': coletas_hoje,
    }
    return render(request, 'app/index.html', context)

# ESTA É A FUNÇÃO QUE ESTÁ FALTANDO OU COM NOME ERRADO:
def coleta_list(request):
    bairros = Bairro.objects.filter(ativo=True)
    bairro_id = request.GET.get('bairro')
    
    agendas = AgendaColeta.objects.filter(ativo=True)
    if bairro_id:
        agendas = agendas.filter(bairro_id=bairro_id)
        
    context = {
        'agendas': agendas,
        'bairros': bairros,
    }
    return render(request, 'app/coleta_lixo.html', context)