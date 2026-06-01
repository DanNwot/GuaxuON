from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from datetime import datetime
from .models import AgendaColeta, Bairro, TipoResiduo

# --- VIEW DO DASHBOARD (RESTRITA) ---
@login_required
def dashboard_view(request):
    """Esta página só abre se o usuário estiver autenticado"""
    return render(request, 'app/base.html')


# --- VIEW DA TELA PRINCIPAL (INDEX) ---
def index(request):
    dias = [
        'Segunda-feira', 'Terça-feira', 'Quarta-feira', 
        'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'
    ]
    hoje_num = datetime.now().weekday()
    dia_atual = dias[hoje_num]

    coletas_hoje = AgendaColeta.objects.filter(
        dia_semana=dia_atual, 
        ativo=True
    ).select_related('bairro', 'tipo').order_by('horario')

    context = {
        'dia_atual': dia_atual,
        'coletas_hoje': coletas_hoje,
    }
    return render(request, 'app/index.html', context)


# --- VIEW DA LIS DE COLETAS COM FILTRO (DADOS FICTÍCIOS REFORÇADOS) ---
def coleta_list(request):
    # 1. Tenta buscar os bairros reais do banco de dados
    bairros_queryset = Bairro.objects.filter(ativo=True).order_by('nome')
    
    # Se o banco de bairros estiver zerado, cria a lista base na memória para renderizar o select
    if not bairros_queryset.exists():
        bairros = [
            Bairro(id=1, nome="Centro"),
            Bairro(id=2, nome="Avenida"),
            Bairro(id=3, nome="Colina dos Prados"),
            Bairro(id=4, nome="Jardim Planalto"),
        ]
    else:
        bairros = list(bairros_queryset)

    # 2. Captura o parâmetro enviado pelo formulário HTML
    bairro_param = request.GET.get('bairro', '').strip()
    bairro_selecionado = None

    # 3. Tenta buscar as agendas reais salvas no banco de dados
    agendas_queryset = AgendaColeta.objects.filter(ativo=True).select_related('bairro', 'tipo')
    
    if agendas_queryset.exists():
        # SE JÁ EXISTIREM DADOS REAIS NO BANCO, REALIZA O FILTRO REAL
        if bairro_param:
            if bairro_param.isdigit():
                bairro_selecionado = int(bairro_param)
                agendas = agendas_queryset.filter(bairro_id=bairro_selecionado)
            else:
                agendas = agendas_queryset.filter(bairro__nome__icontains=bairro_param)
                bairro_obj = Bairro.objects.filter(nome__icontains=bairro_param).first()
                if bairro_obj:
                    bairro_selecionado = bairro_obj.id
        else:
            agendas = agendas_queryset
            
        agendas = agendas.order_by('bairro__nome', 'dia_semana', 'horario')
    else:
        # SE O BANCO ESTIVER TOTALMENTE VAZIO, CRIA AUTOMATICAMENTE EXATAMENTE 5 HORÁRIOS PARA CADA BAIRRO
        tipo_organico = TipoResiduo(nome="Orgânico", cor_identificacao="#004a8d")
        tipo_reciclavel = TipoResiduo(nome="Reciclável", cor_identificacao="#28a745")
        tipo_eletronico = TipoResiduo(nome="Eletrônico", cor_identificacao="#ffc107")

        # Objetos de bairros mapeados com chaves numéricas
        b1 = Bairro(id=1, nome="Centro")
        b2 = Bairro(id=2, nome="Avenida")
        b3 = Bairro(id=3, nome="Colina dos Prados")
        b4 = Bairro(id=4, nome="Jardim Planalto")

        dados_ficticios = [
            # === 5 HORÁRIOS: CENTRO ===
            AgendaColeta(bairro=b1, tipo=tipo_organico, dia_semana="Segunda-feira", horario="07:00"),
            AgendaColeta(bairro=b1, tipo=tipo_reciclavel, dia_semana="Terça-feira", horario="09:00"),
            AgendaColeta(bairro=b1, tipo=tipo_organico, dia_semana="Quarta-feira", horario="07:00"),
            AgendaColeta(bairro=b1, tipo=tipo_reciclavel, dia_semana="Quinta-feira", horario="14:30"),
            AgendaColeta(bairro=b1, tipo=tipo_eletronico, dia_semana="Sábado", horario="08:00"),

            # === 5 HORÁRIOS: AVENIDA ===
            AgendaColeta(bairro=b2, tipo=tipo_organico, dia_semana="Terça-feira", horario="08:30"),
            AgendaColeta(bairro=b2, tipo=tipo_organico, dia_semana="Quinta-feira", horario="08:30"),
            AgendaColeta(bairro=b2, tipo=tipo_reciclavel, dia_semana="Sexta-feira", horario="10:00"),
            AgendaColeta(bairro=b2, tipo=tipo_organico, dia_semana="Sábado", horario="07:15"),
            AgendaColeta(bairro=b2, tipo=tipo_eletronico, dia_semana="Domingo", horario="19:00"),

            # === 5 HORÁRIOS: COLINA DOS PRADOS ===
            AgendaColeta(bairro=b3, tipo=tipo_organico, dia_semana="Segunda-feira", horario="13:00"),
            AgendaColeta(bairro=b3, tipo=tipo_reciclavel, dia_semana="Quarta-feira", horario="10:30"),
            AgendaColeta(bairro=b3, tipo=tipo_organico, dia_semana="Quinta-feira", horario="13:00"),
            AgendaColeta(bairro=b3, tipo=tipo_reciclavel, dia_semana="Sexta-feira", horario="16:00"),
            AgendaColeta(bairro=b3, tipo=tipo_eletronico, dia_semana="Sábado", horario="11:15"),

            # === 5 HORÁRIOS: JARDIM PLANALTO ===
            AgendaColeta(bairro=b4, tipo=tipo_organico, dia_semana="Segunda-feira", horario="06:30"),
            AgendaColeta(bairro=b4, tipo=tipo_reciclavel, dia_semana="Terça-feira", horario="14:00"),
            AgendaColeta(bairro=b4, tipo=tipo_organico, dia_semana="Quarta-feira", horario="06:30"),
            AgendaColeta(bairro=b4, tipo=tipo_organico, dia_semana="Sexta-feira", horario="06:30"),
            AgendaColeta(bairro=b4, tipo=tipo_eletronico, dia_semana="Sábado", horario="15:30"),
        ]

        # Tratamento de filtragem na memória
        if bairro_param:
            if bairro_param.isdigit():
                bairro_selecionado = int(bairro_param)
                agendas = [a for a in dados_ficticios if a.bairro.id == bairro_selecionado]
            else:
                bairro_selecionado = bairro_param
                agendas = [a for a in dados_ficticios if bairro_param.lower() in a.bairro.nome.lower()]
        else:
            agendas = dados_ficticios

    context = {
        'agendas': agendas,
        'bairros': bairros,
        'bairro_selecionado': bairro_selecionado,
    }
    
    return render(request, 'app/coleta_lixo.html', context)


# --- VIEW DE CADASTRO DE NOVOS USUÁRIOS ---
def register_view(request):
    """Gera o formulário para criação de novas contas de cidadãos"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) 
            return redirect('dashboard') 
    else:
        form = UserCreationForm()
    
    # 🌟 CORREÇÃO AQUI: Apontando para o caminho exato dentro de app/templates/app/registration/
    return render(request, 'app/registration/register.html', {'form': form})


# --- VIEW DE PERFIL DO USUÁRIO ---
@login_required
def perfil_view(request):
    """Exibe os dados do usuário autenticado no sistema"""
    return render(request, 'app/perfil.html', {'usuario': request.user})